from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ResearchPaths:
    root: Path
    snapshots: Path
    observations: Path
    marker: Path


class ResearchService:
    """Persistent ACEMD-side research and observation storage.

    ACE databases remain read-only. Research artifacts are written only to the
    configured ACEMD evidence directory. The storage root must be supplied by
    ``ACEMD_RESEARCH_ROOT`` (or explicitly by the caller); no container-local
    fallback is permitted because rebuilds would destroy the evidence.
    """

    def __init__(self, ace_data_service: Any, root: str | Path | None = None):
        self.ace_data_service = ace_data_service
        configured_root = root or os.environ.get("ACEMD_RESEARCH_ROOT", "").strip()
        if not configured_root:
            raise RuntimeError(
                "ACEMD_RESEARCH_ROOT is not configured. Research Lab refuses "
                "to use ephemeral container storage."
            )

        root_path = Path(configured_root).expanduser()
        if not root_path.is_absolute():
            raise RuntimeError("ACEMD_RESEARCH_ROOT must be an absolute path.")

        self.paths = ResearchPaths(
            root=root_path,
            snapshots=root_path / "snapshots",
            observations=root_path / "observations.json",
            marker=root_path / ".acemd-research-store",
        )
        self._initialize_store()

    def _initialize_store(self) -> None:
        self.paths.root.mkdir(parents=True, exist_ok=True)
        self.paths.snapshots.mkdir(parents=True, exist_ok=True)
        # Do not rewrite an existing marker on every startup. Older test
        # deployments may contain a root-owned but readable marker; preserving
        # it allows the dashboard to move safely to the configured host UID/GID.
        if not self.paths.marker.exists():
            self.paths.marker.write_text(
                "ACE Management Dashboard persistent Research Lab evidence store\n",
                encoding="utf-8",
            )
        if not self.paths.observations.exists():
            self._write_json(self.paths.observations, [])
        self._assert_writable()

    def _assert_writable(self) -> None:
        probe = self.paths.root / f".write-test-{uuid.uuid4().hex}"
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
        except OSError as exc:
            raise RuntimeError(
                f"Research Lab evidence store is not writable: {self.paths.root}: {exc}"
            ) from exc

    def get_dashboard(self) -> dict[str, Any]:
        snapshots = self.list_snapshots()
        observations = self.list_observations()
        storage = self.get_storage_status()
        return {
            "summary": {
                "snapshots": len(snapshots),
                "observations": len(observations),
                "mode": "ACE read-only / persistent ACEMD evidence store",
                "storage": str(self.paths.root),
                "storage_status": storage,
            },
            "snapshots": snapshots[:50],
            "observations": observations[:25],
        }

    def get_storage_status(self) -> dict[str, Any]:
        exists = self.paths.root.is_dir()
        writable = exists and os.access(self.paths.root, os.W_OK)
        return {
            "configured": True,
            "absolute": self.paths.root.is_absolute(),
            "exists": exists,
            "writable": writable,
            "persistent": True,
            "path": str(self.paths.root),
            "label": "Persistent and writable" if writable else "Storage problem",
        }

    def create_snapshot(self, character_id: int, label: str = "", notes: str = "", expected_state: str = "") -> dict[str, Any]:
        snapshot = self.ace_data_service.get_character_snapshot(character_id)
        now = self._now()
        snapshot_id = f"snap-{now.replace(':', '').replace('-', '').replace('.', '')}-{uuid.uuid4().hex[:8]}"
        snapshot.update({
            "snapshot_id": snapshot_id,
            "created_at": now,
            "label": label.strip() or f"Character {character_id} snapshot",
            "notes": notes.strip(),
            "expected_state": expected_state.strip(),
            "storage_version": 2,
            "storage_root": str(self.paths.root),
        })
        self._write_json(self._snapshot_path(snapshot_id), snapshot)
        return {"ok": True, "snapshot": self._snapshot_summary(snapshot)}

    def create_observation(self, title: str, before_snapshot_id: str, after_snapshot_id: str, action_notes: str = "", outcome_notes: str = "") -> dict[str, Any]:
        before = self.read_snapshot(before_snapshot_id)
        after = self.read_snapshot(after_snapshot_id)
        if not before or not after:
            return {"ok": False, "error": "Both before and after snapshots are required."}
        if before.get("character_id") != after.get("character_id"):
            return {"ok": False, "error": "Snapshots must belong to the same character."}
        diff = self.diff_snapshots(before, after)
        observations = self.list_observations(oldest_first=True)
        obs_id = f"OBS-{len(observations) + 1:04d}"
        observation = {
            "observation_id": obs_id,
            "title": title.strip() or obs_id,
            "created_at": self._now(),
            "character_id": before.get("character_id"),
            "character_name": after.get("character", {}).get("name") or before.get("character", {}).get("name"),
            "before_snapshot_id": before_snapshot_id,
            "after_snapshot_id": after_snapshot_id,
            "action_notes": action_notes.strip(),
            "outcome_notes": outcome_notes.strip(),
            "diff_summary": diff["summary"],
            "diff": diff,
            "storage_version": 2,
        }
        observations.append(observation)
        self._write_json(self.paths.observations, observations)
        return {"ok": True, "observation": observation}

    def list_snapshots(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for path in sorted(self.paths.snapshots.glob("*.json"), reverse=True):
            data = self._read_json(path, {})
            if data:
                rows.append(self._snapshot_summary(data))
        return rows

    def list_observations(self, oldest_first: bool = False) -> list[dict[str, Any]]:
        rows = self._read_json(self.paths.observations, [])
        rows = rows if isinstance(rows, list) else []
        return rows if oldest_first else list(reversed(rows))

    def read_snapshot(self, snapshot_id: str) -> dict[str, Any] | None:
        path = self._snapshot_path(self._safe_id(snapshot_id))
        if not path.exists():
            return None
        data = self._read_json(path, {})
        return data if isinstance(data, dict) else None

    def get_observation(self, observation_id: str) -> dict[str, Any] | None:
        for row in self.list_observations(oldest_first=True):
            if row.get("observation_id") == observation_id:
                return row
        return None

    def diff_snapshots(self, before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
        groups: list[dict[str, Any]] = []
        summary = {"tables_changed": 0, "rows_added": 0, "rows_removed": 0, "rows_changed": 0}
        before_tables = before.get("tables", {}) if isinstance(before.get("tables"), dict) else {}
        after_tables = after.get("tables", {}) if isinstance(after.get("tables"), dict) else {}
        for table in sorted(set(before_tables) | set(after_tables)):
            before_rows = before_tables.get(table, []) or []
            after_rows = after_tables.get(table, []) or []
            table_diff = self._diff_rows(table, before_rows, after_rows)
            if table_diff["added"] or table_diff["removed"] or table_diff["changed"]:
                summary["tables_changed"] += 1
                summary["rows_added"] += len(table_diff["added"])
                summary["rows_removed"] += len(table_diff["removed"])
                summary["rows_changed"] += len(table_diff["changed"])
                groups.append(table_diff)
        return {"summary": summary, "groups": groups}

    def _diff_rows(self, table: str, before_rows: list[dict[str, Any]], after_rows: list[dict[str, Any]]) -> dict[str, Any]:
        before_map = {self._row_key(table, row, i): row for i, row in enumerate(before_rows)}
        after_map = {self._row_key(table, row, i): row for i, row in enumerate(after_rows)}
        added = [{"key": k, "row": after_map[k]} for k in sorted(set(after_map) - set(before_map))]
        removed = [{"key": k, "row": before_map[k]} for k in sorted(set(before_map) - set(after_map))]
        changed = []
        for key in sorted(set(before_map) & set(after_map)):
            before = before_map[key]
            after = after_map[key]
            changes = []
            for col in sorted(set(before) | set(after)):
                if before.get(col) != after.get(col):
                    changes.append({"column": col, "before": before.get(col), "after": after.get(col)})
            if changes:
                changed.append({"key": key, "changes": changes, "before": before, "after": after})
        return {"table": table, "added": added, "removed": removed, "changed": changed}

    def _row_key(self, table: str, row: dict[str, Any], index: int) -> str:
        lowered = {str(k).lower(): k for k in row.keys()}
        parts = []
        for candidate in ("object_id", "type", "key", "id", "position_type", "spell", "destination_type"):
            real = lowered.get(candidate)
            if real is not None:
                parts.append(f"{candidate}={row.get(real)}")
        return "|".join(parts) if parts else f"row={index}"

    def _snapshot_summary(self, data: dict[str, Any]) -> dict[str, Any]:
        tables = data.get("tables", {}) if isinstance(data.get("tables"), dict) else {}
        rows = sum(len(v or []) for v in tables.values())
        return {
            "snapshot_id": data.get("snapshot_id", ""),
            "created_at": data.get("created_at", ""),
            "label": data.get("label", ""),
            "character_id": data.get("character_id"),
            "character_name": (data.get("character") or {}).get("name", ""),
            "account_name": (data.get("character") or {}).get("accountName", ""),
            "table_count": len(tables),
            "row_count": rows,
            "notes": data.get("notes", ""),
            "expected_state": data.get("expected_state", ""),
            "error": data.get("error", ""),
        }

    def _snapshot_path(self, snapshot_id: str) -> Path:
        return self.paths.snapshots / f"{self._safe_id(snapshot_id)}.json"

    @staticmethod
    def _safe_id(value: str) -> str:
        return "".join(ch for ch in str(value) if ch.isalnum() or ch in "-_")[:120]

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    @staticmethod
    def _read_json(path: Path, default: Any) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default

    @staticmethod
    def _write_json(path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(path.suffix + f".{uuid.uuid4().hex}.tmp")
        temp.write_text(json.dumps(data, indent=2, sort_keys=True, default=str), encoding="utf-8")
        temp.replace(path)
