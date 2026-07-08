from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


class EventService:
    """Lightweight operational event journal for ACE dashboard state changes.

    The service records compact JSONL events under the runtime backup area so the
    dashboard can show what changed without requiring a database migration or a
    background worker.  Health observations are idempotent: repeated refreshes
    of the same state do not create duplicate events.
    """

    def __init__(self, root_path: str | Path | None = None):
        self.root_path = Path(root_path or os.environ.get("ACE_ROOT", "/opt/acserver")).resolve()
        runtime_dir = Path(os.environ.get("ACE_RUNTIME_DIR", self.root_path / "backups" / "runtime"))
        self.events_path = Path(os.environ.get("ACE_EVENTS_LOG", runtime_dir / "operational-events.jsonl"))
        self.state_path = Path(os.environ.get("ACE_EVENTS_STATE", runtime_dir / "health-state.json"))
        self.max_events = int(os.environ.get("ACE_EVENTS_MAX", "500"))

    def observe_health(self, health: dict[str, Any]) -> list[dict[str, Any]]:
        """Compare the latest health snapshot to the last seen snapshot.

        Returns the newly-created events, if any.  Failures in persistence are
        returned as a single warning event but never raise into the page route.
        """
        try:
            snapshot = self._snapshot_from_health(health)
            previous = self._read_state()
            events = self._diff_snapshots(previous, snapshot)
            if not previous:
                events.insert(0, self._event(
                    source="health",
                    event_type="health_snapshot_initialized",
                    severity=snapshot.get("overall_level", "info"),
                    title="Health monitoring initialized",
                    message=f"Initial observed state: {snapshot.get('overall_label', 'Unknown')}.",
                    entity="ACE Stack",
                    previous=None,
                    current=snapshot.get("overall_label"),
                ))
            if events:
                self._append_events(events)
            self._write_state(snapshot)
            return events
        except Exception as exc:
            return [self._event(
                source="events",
                event_type="event_recording_failed",
                severity="warning",
                title="Event recording failed",
                message=str(exc),
                entity="Event Journal",
            )]

    def record_management_result(self, result: dict[str, Any]) -> None:
        """Record a management command result as an operational event."""
        severity = "info" if result.get("success") else "warning"
        if result.get("exit_code") not in (0, None) and not result.get("success"):
            severity = "warning"
        title = "Management command completed" if result.get("success") else "Management command failed"
        if result.get("dry_run"):
            title = "Management dry run completed" if result.get("success") else "Management dry run failed"
        event = self._event(
            source="management",
            event_type="management_action",
            severity=severity,
            title=title,
            message=f"{result.get('command', 'manage.sh')} exited with code {result.get('exit_code', 'unknown')}.",
            entity=result.get("label") or result.get("action_id") or "Management",
            current="OK" if result.get("success") else "Failed",
            metadata={
                "action_id": result.get("action_id"),
                "command": result.get("command"),
                "exit_code": result.get("exit_code"),
                "dry_run": result.get("dry_run", False),
            },
        )
        self._append_events([event])

    def get_recent_events(self, limit: int = 25, severity: str | None = None, source: str | None = None) -> list[dict[str, Any]]:
        rows = self._read_events()
        if severity:
            rows = [r for r in rows if r.get("severity") == severity]
        if source:
            rows = [r for r in rows if r.get("source") == source]
        return list(reversed(rows[-max(1, min(int(limit), 200)):]))

    def get_summary(self) -> dict[str, Any]:
        rows = self._read_events()
        recent = rows[-50:]
        return {
            "total": len(rows),
            "recent": len(recent),
            "critical": sum(1 for r in recent if r.get("severity") == "critical"),
            "warning": sum(1 for r in recent if r.get("severity") == "warning"),
            "info": sum(1 for r in recent if r.get("severity") == "info"),
            "latest": rows[-1] if rows else None,
        }

    def _snapshot_from_health(self, health: dict[str, Any]) -> dict[str, Any]:
        services = {}
        for row in health.get("services", []) or []:
            name = row.get("name") or row.get("label")
            if not name:
                continue
            services[name] = {
                "label": row.get("label", name),
                "state": row.get("state", "Unknown"),
                "health": row.get("health", "Unknown"),
                "level": row.get("level", "unknown"),
            }
        checks = {}
        for row in health.get("checks", []) or []:
            name = row.get("name")
            if not name:
                continue
            checks[name] = {
                "status": row.get("status", "Unknown"),
                "level": row.get("level", "unknown"),
                "detail": row.get("detail", ""),
            }
        return {
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "overall_level": health.get("overall", {}).get("level", "unknown"),
            "overall_label": health.get("overall", {}).get("label", "Unknown"),
            "services": services,
            "checks": checks,
        }

    def _diff_snapshots(self, previous: dict[str, Any], current: dict[str, Any]) -> list[dict[str, Any]]:
        if not previous:
            return []
        events: list[dict[str, Any]] = []
        prev_level = previous.get("overall_level")
        cur_level = current.get("overall_level")
        if prev_level != cur_level:
            events.append(self._event(
                source="health",
                event_type="overall_health_changed",
                severity=self._severity_for_level(cur_level),
                title="Overall health changed",
                message=f"ACE stack changed from {previous.get('overall_label', prev_level)} to {current.get('overall_label', cur_level)}.",
                entity="ACE Stack",
                previous=previous.get("overall_label", prev_level),
                current=current.get("overall_label", cur_level),
            ))

        for name, cur in current.get("services", {}).items():
            prev = previous.get("services", {}).get(name)
            if not prev:
                events.append(self._event(
                    source="health",
                    event_type="service_observed",
                    severity=self._severity_for_level(cur.get("level")),
                    title="Service observed",
                    message=f"{cur.get('label', name)} is {cur.get('state')} / {cur.get('health')}.",
                    entity=cur.get("label", name),
                    previous=None,
                    current=cur.get("level"),
                ))
                continue
            if prev.get("level") != cur.get("level") or prev.get("state") != cur.get("state") or prev.get("health") != cur.get("health"):
                events.append(self._event(
                    source="health",
                    event_type="service_state_changed",
                    severity=self._severity_for_level(cur.get("level")),
                    title="Service state changed",
                    message=f"{cur.get('label', name)} changed from {prev.get('state')} / {prev.get('health')} to {cur.get('state')} / {cur.get('health')}.",
                    entity=cur.get("label", name),
                    previous=f"{prev.get('state')} / {prev.get('health')}",
                    current=f"{cur.get('state')} / {cur.get('health')}",
                ))

        for name, prev in previous.get("services", {}).items():
            if name not in current.get("services", {}):
                events.append(self._event(
                    source="health",
                    event_type="service_missing",
                    severity="critical",
                    title="Service disappeared",
                    message=f"{prev.get('label', name)} was present in the prior snapshot and is no longer reported.",
                    entity=prev.get("label", name),
                    previous=prev.get("state"),
                    current="Missing",
                ))
        return events

    def _event(self, *, source: str, event_type: str, severity: str, title: str, message: str, entity: str, previous: str | None = None, current: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "timestamp": now.isoformat(),
            "display_time": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "source": source,
            "type": event_type,
            "severity": severity if severity in {"info", "ok", "warning", "critical"} else "info",
            "title": title,
            "message": message,
            "entity": entity,
            "previous": previous,
            "current": current,
            "metadata": metadata or {},
        }

    def _severity_for_level(self, level: str | None) -> str:
        if level == "critical":
            return "critical"
        if level == "warning":
            return "warning"
        if level == "ok":
            return "info"
        return "warning"

    def _read_state(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return {}
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _write_state(self, snapshot: dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")

    def _read_events(self) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        rows = []
        try:
            for line in self.events_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(json.loads(line))
        except Exception:
            return []
        return rows

    def _append_events(self, events: Iterable[dict[str, Any]]) -> None:
        events = list(events)
        if not events:
            return
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        existing = self._read_events()
        combined = [*existing, *events]
        if len(combined) > self.max_events:
            combined = combined[-self.max_events:]
        with self.events_path.open("w", encoding="utf-8") as handle:
            for row in combined:
                handle.write(json.dumps(row, sort_keys=True) + "\n")
