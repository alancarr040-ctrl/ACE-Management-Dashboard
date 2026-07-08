from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class LogSource:
    key: str
    label: str
    container: str
    default_lines: int = 150


class ACELogService:
    SOURCES: tuple[LogSource, ...] = (
        LogSource("ace-server", "ACE Server", "ace-server", 150),
        LogSource("ace-db", "ACE Database", "ace-db", 150),
        LogSource("ace-dashboard", "ACE Dashboard", "ace-dashboard", 150),
    )

    SEVERITIES: tuple[str, ...] = ("all", "error", "warning", "info")

    def __init__(self, docker_service):
        self.docker_service = docker_service

    def get_sources(self) -> list[dict[str, str]]:
        return [{"key": source.key, "label": source.label, "container": source.container} for source in self.SOURCES]

    def get_view(self, source_key: str = "ace-server", lines: int = 150, severity: str = "all", search: str = "") -> dict:
        source = self._resolve_source(source_key)
        safe_lines = self._safe_lines(lines, source.default_lines)
        safe_severity = severity if severity in self.SEVERITIES else "all"
        safe_search = (search or "").strip()[:120]

        raw = self.docker_service.get_container_logs(source.container, lines=safe_lines)
        entries = self._parse_lines(raw.splitlines())
        filtered = self._filter_entries(entries, safe_severity, safe_search)

        return {
            "source": source.key,
            "source_label": source.label,
            "container": source.container,
            "lines": safe_lines,
            "severity": safe_severity,
            "search": safe_search,
            "entries": filtered,
            "entry_count": len(filtered),
            "raw_count": len(entries),
            "summary": self._summarize(entries),
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }

    def _resolve_source(self, key: str) -> LogSource:
        for source in self.SOURCES:
            if source.key == key:
                return source
        return self.SOURCES[0]

    def _safe_lines(self, value: int, default: int) -> int:
        try:
            return max(25, min(int(value), 500))
        except (TypeError, ValueError):
            return default

    def _parse_lines(self, lines: Iterable[str]) -> list[dict[str, str]]:
        entries: list[dict[str, str]] = []
        for line in lines:
            text = line.strip()
            if not text:
                continue
            timestamp = ""
            message = text
            if len(text) > 20 and text[10:11] == "T":
                first, _, rest = text.partition(" ")
                if first:
                    timestamp = first.replace("T", " ").replace("Z", " UTC")
                    message = rest or text
            severity = self._severity(message)
            entries.append({"timestamp": timestamp, "severity": severity, "message": message})
        return entries

    def _severity(self, message: str) -> str:
        lower = message.lower()
        if any(token in lower for token in ("error", "exception", "failed", "failure", "denied", "timeout", "critical", "fatal")):
            return "error"
        if any(token in lower for token in ("warn", "retry", "degraded")):
            return "warning"
        return "info"

    def _filter_entries(self, entries: list[dict[str, str]], severity: str, search: str) -> list[dict[str, str]]:
        result = entries
        if severity != "all":
            result = [entry for entry in result if entry["severity"] == severity]
        if search:
            needle = search.lower()
            result = [entry for entry in result if needle in entry["message"].lower() or needle in entry["timestamp"].lower()]
        return result

    def _summarize(self, entries: list[dict[str, str]]) -> dict[str, int]:
        return {
            "total": len(entries),
            "errors": sum(1 for entry in entries if entry["severity"] == "error"),
            "warnings": sum(1 for entry in entries if entry["severity"] == "warning"),
            "info": sum(1 for entry in entries if entry["severity"] == "info"),
        }
