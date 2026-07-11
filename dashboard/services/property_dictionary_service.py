from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class PropertyDictionaryService:
    """Read-only ACE property dictionary backed by versioned project data."""

    GROUP_ALIASES = {
        "ints": "int",
        "strings": "string",
        "floats": "float",
        "bools": "bool",
        "positions": "position",
        "dids": "did",
        "iids": "iid",
        "int64s": "int64",
    }

    def __init__(self, path: str | Path | None = None):
        self.path = self._resolve_path(path)
        self._payload: dict[str, Any] = {}
        self._entries: list[dict[str, Any]] = []
        self._index: dict[tuple[str, int], dict[str, Any]] = {}
        self.load_error = ""
        self.reload()

    @staticmethod
    def _resolve_path(path: str | Path | None = None) -> Path:
        """Resolve runtime dictionary path without depending on the image-only data directory."""
        if path:
            return Path(path)

        configured = os.environ.get("ACEMD_PROPERTY_DICTIONARY", "").strip()
        if configured:
            return Path(configured)

        data_root = Path(os.environ.get("ACEMD_DATA_ROOT", "/app/data"))
        runtime_path = data_root / "property_dictionary.json"
        if runtime_path.exists():
            return runtime_path

        # Development/source-tree fallback. In production /app/data is a bind mount,
        # so release packages also install the dictionary at data/property_dictionary.json.
        return Path(__file__).resolve().parents[1] / "data" / "property_dictionary.json"

    def reload(self) -> None:
        self.load_error = ""
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except OSError as exc:
            self.load_error = f"Unable to read property dictionary at {self.path}: {exc}"
            payload = {"schema_version": 1, "entries": [], "source": {}}
        except json.JSONDecodeError as exc:
            self.load_error = f"Invalid property dictionary JSON at {self.path}: {exc}"
            payload = {"schema_version": 1, "entries": [], "source": {}}
        entries = payload.get("entries", [])
        self._payload = payload if isinstance(payload, dict) else {}
        self._entries = [row for row in entries if isinstance(row, dict)]
        self._index = {}
        for row in self._entries:
            try:
                key = (self.normalize_group(row.get("group", "")), int(row.get("type")))
            except (TypeError, ValueError):
                continue
            self._index[key] = row

    @classmethod
    def normalize_group(cls, group: str) -> str:
        key = str(group or "").strip().lower()
        return cls.GROUP_ALIASES.get(key, key)

    def lookup(self, group: str, property_type: Any) -> dict[str, Any]:
        normalized = self.normalize_group(group)
        try:
            type_id = int(property_type)
        except (TypeError, ValueError):
            type_id = -1
        found = self._index.get((normalized, type_id))
        if found:
            return dict(found)
        return {
            "group": normalized,
            "type": type_id,
            "name": "UNKNOWN_PROPERTY",
            "friendly_name": "Unknown Property",
            "description": "",
            "lookup": "",
            "notes": "",
            "reference": "",
            "status": "unknown",
            "origin": "Unmapped",
            "source": "",
            "source_row": None,
        }

    def annotate_rows(self, group: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        annotated = []
        for row in rows or []:
            item = dict(row)
            type_value = self._case_value(item, "type")
            definition = self.lookup(group, type_value)
            item["_property"] = definition
            annotated.append(item)
        return annotated

    def browse(
        self,
        search: str = "",
        group: str = "all",
        status: str = "all",
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        page = max(1, int(page or 1))
        per_page = min(200, max(25, int(per_page or 50)))
        query = str(search or "").strip().lower()
        group = self.normalize_group(group) if group != "all" else "all"
        status = str(status or "all").strip().lower()

        rows = []
        for entry in self._entries:
            if group != "all" and self.normalize_group(entry.get("group", "")) != group:
                continue
            if status != "all" and str(entry.get("status", "")).lower() != status:
                continue
            haystack = " ".join(str(entry.get(k, "")) for k in (
                "group", "type", "name", "friendly_name", "description", "lookup", "notes", "origin"
            )).lower()
            if query and query not in haystack:
                continue
            rows.append(dict(entry))

        rows.sort(key=lambda r: (self.normalize_group(r.get("group", "")), int(r.get("type", 0)), r.get("name", "")))
        total = len(rows)
        pages = max(1, (total + per_page - 1) // per_page) if total else 0
        if pages and page > pages:
            page = pages
        start = (page - 1) * per_page
        page_rows = rows[start:start + per_page]

        status_counts = {"confirmed": 0, "research": 0, "unknown": 0}
        group_counts: dict[str, int] = {}
        for entry in self._entries:
            entry_status = str(entry.get("status", "unknown")).lower()
            status_counts[entry_status] = status_counts.get(entry_status, 0) + 1
            entry_group = self.normalize_group(entry.get("group", ""))
            group_counts[entry_group] = group_counts.get(entry_group, 0) + 1

        return {
            "summary": {
                "entries": len(self._entries),
                "confirmed": status_counts.get("confirmed", 0),
                "research": status_counts.get("research", 0),
                "groups": len(group_counts),
                "dictionary_version": self._payload.get("dictionary_version", ""),
                "source": (self._payload.get("source") or {}).get("name", ""),
                "path": str(self.path),
                "load_error": self.load_error,
            },
            "rows": page_rows,
            "filters": {"q": search, "group": group, "status": status},
            "groups": sorted(group_counts),
            "group_counts": group_counts,
            "status_counts": status_counts,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "total": total,
        }

    @staticmethod
    def _case_value(row: dict[str, Any], key: str) -> Any:
        for current_key, value in row.items():
            if str(current_key).lower() == key.lower():
                return value
        return None
