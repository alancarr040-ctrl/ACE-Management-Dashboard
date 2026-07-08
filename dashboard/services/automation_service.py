from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


class AutomationService:
    """Request-driven ACEMD automation scheduler.

    Phase 2.7.0 intentionally avoids introducing a daemon, cron editor, or write-capable
    automation.  The dashboard performs a safe scheduler tick whenever the Automation
    page or API is read.  Jobs are read-only checks that can publish events, update job
    history, and establish the scheduling model future phases will expand.
    """

    def __init__(self, health_service, backup_service, system_service, management_service, event_service, root_path: str | Path | None = None):
        self.health_service = health_service
        self.backup_service = backup_service
        self.system_service = system_service
        self.management_service = management_service
        self.event_service = event_service
        self.root_path = Path(root_path or os.environ.get("ACE_ROOT", "/opt/acserver")).resolve()
        runtime_dir = Path(os.environ.get("ACE_RUNTIME_DIR", self.root_path / "backups" / "runtime"))
        self.state_path = Path(os.environ.get("ACEMD_AUTOMATION_STATE", runtime_dir / "automation-state.json"))
        self.max_history = int(os.environ.get("ACEMD_AUTOMATION_HISTORY_MAX", "100"))
        self.jobs = self._default_jobs()

    def get_status(self, run_due: bool = True) -> dict[str, Any]:
        if run_due:
            self.run_due_jobs()
        state = self._read_state()
        jobs = [self._job_view(job, state) for job in self.jobs]
        enabled = sum(1 for j in jobs if j["enabled"])
        disabled = len(jobs) - enabled
        last_runs = [j for j in jobs if j.get("last_run")]
        last_run = max((j["last_run"] for j in last_runs), default="Never")
        next_due_candidates = [j["next_run"] for j in jobs if j.get("enabled") and j.get("next_run")]
        next_run = min(next_due_candidates) if next_due_candidates else "None"
        failures = sum(1 for j in jobs if j.get("last_result_level") in ("warning", "critical"))
        return {
            "engine": {
                "status": "Running",
                "mode": "Request-driven",
                "jobs": len(jobs),
                "enabled": enabled,
                "disabled": disabled,
                "last_tick": state.get("last_tick", "Never"),
                "last_run": last_run,
                "next_run": next_run,
                "failures": failures,
            },
            "jobs": jobs,
            "history": list(reversed(state.get("history", [])[-self.max_history:])),
        }

    def run_due_jobs(self) -> list[dict[str, Any]]:
        now = self._now()
        state = self._read_state()
        state["last_tick"] = self._format_time(now)
        results = []
        for job in self.jobs:
            if not job.get("enabled", True):
                continue
            current = state.setdefault("jobs", {}).setdefault(job["id"], {})
            next_run = self._parse_time(current.get("next_run"))
            if next_run is None or now >= next_run:
                results.append(self.run_job(job["id"], state=state, manual=False))
        self._write_state(state)
        return results

    def run_job(self, job_id: str, state: dict[str, Any] | None = None, manual: bool = True) -> dict[str, Any]:
        job = next((j for j in self.jobs if j["id"] == job_id), None)
        if not job:
            return {"job_id": job_id, "success": False, "level": "critical", "message": "Unknown job."}
        own_state = state is None
        if state is None:
            state = self._read_state()
        now = self._now()
        job_state = state.setdefault("jobs", {}).setdefault(job_id, {})
        try:
            result = job["runner"]()
            success = result.get("level") not in ("critical", "warning")
        except Exception as exc:
            result = {"level": "critical", "status": "Failed", "detail": str(exc)}
            success = False
        next_run = now + timedelta(seconds=int(job["interval_seconds"]))
        history_row = {
            "timestamp": self._format_time(now),
            "job_id": job_id,
            "job_name": job["name"],
            "manual": manual,
            "success": success,
            "level": result.get("level", "info"),
            "status": result.get("status", "Completed"),
            "detail": result.get("detail", ""),
        }
        job_state.update({
            "last_run": history_row["timestamp"],
            "next_run": self._format_time(next_run),
            "last_result_level": history_row["level"],
            "last_result": history_row["status"],
            "last_detail": history_row["detail"],
        })
        state.setdefault("history", []).append(history_row)
        state["history"] = state["history"][-self.max_history:]
        self.event_service.record_event(
            source="automation",
            event_type="automation_job_completed",
            severity="warning" if history_row["level"] == "warning" else "critical" if history_row["level"] == "critical" else "info",
            title=f"Automation job {'manual run' if manual else 'completed'}",
            message=f"{job['name']}: {history_row['status']}. {history_row['detail']}",
            entity=job["name"],
            current=history_row["status"],
            metadata={"job_id": job_id, "manual": manual},
        )
        if own_state:
            state["last_tick"] = self._format_time(now)
            self._write_state(state)
        return history_row

    def _default_jobs(self) -> list[dict[str, Any]]:
        return [
            self._job("health_monitor", "Health Monitor", "Core", "Every 30 seconds", 30, "Runs the read-only ACEMD health aggregation and records health transitions.", self._run_health_monitor),
            self._job("backup_verification", "Backup Verification", "Backups", "Hourly", 3600, "Verifies that ACEMD can see current backup inventory and backup status.", self._run_backup_verification),
            self._job("disk_usage_check", "Disk Usage Check", "System", "Every 5 minutes", 300, "Checks project filesystem usage against operational thresholds.", self._run_disk_check),
            self._job("wrapper_validation", "Wrapper Validation", "Management", "Every 5 minutes", 300, "Verifies that the management wrapper is installed and executable.", self._run_wrapper_validation),
            self._job("event_journal_check", "Event Journal Check", "Events", "Hourly", 3600, "Verifies that the operational event journal is readable and retaining events.", self._run_event_journal_check),
        ]

    def _job(self, job_id: str, name: str, group: str, schedule: str, interval_seconds: int, description: str, runner: Callable[[], dict[str, Any]]):
        return {"id": job_id, "name": name, "group": group, "schedule": schedule, "interval_seconds": interval_seconds, "description": description, "enabled": True, "runner": runner}

    def _job_view(self, job: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
        row = state.get("jobs", {}).get(job["id"], {})
        return {
            "id": job["id"],
            "name": job["name"],
            "group": job["group"],
            "schedule": job["schedule"],
            "description": job["description"],
            "enabled": job.get("enabled", True),
            "last_run": row.get("last_run", "Never"),
            "next_run": row.get("next_run", "Pending"),
            "last_result": row.get("last_result", "Not run"),
            "last_result_level": row.get("last_result_level", "unknown"),
            "last_detail": row.get("last_detail", ""),
        }

    def _run_health_monitor(self) -> dict[str, Any]:
        health = self.health_service.get_health()
        self.event_service.observe_health(health)
        overall = health.get("overall", {})
        return {"level": overall.get("level", "unknown"), "status": overall.get("label", "Unknown"), "detail": overall.get("message", "Health checked.")}

    def _run_backup_verification(self) -> dict[str, Any]:
        backups = self.backup_service.list_backups()
        summary = self.backup_service.get_summary()
        if not backups:
            return {"level": "warning", "status": "No backups found", "detail": "No runtime or baseline backups were discovered."}
        failed = int(summary.get("failed", 0) or 0) + int(summary.get("invalid", 0) or 0)
        latest = backups[0]
        if failed:
            return {"level": "warning", "status": f"{failed} failed/invalid", "detail": f"Latest backup: {latest.get('display_name', latest.get('name', 'Unknown'))}"}
        return {"level": "ok", "status": "Verified", "detail": f"Latest backup: {latest.get('display_name', latest.get('name', 'Unknown'))}"}

    def _run_disk_check(self) -> dict[str, Any]:
        disk = self.system_service.get_disk_usage()
        percent_text = str(disk.get("percent", "0")).replace("%", "").strip()
        try:
            percent = float(percent_text)
        except ValueError:
            percent = 0.0
        if percent >= 90:
            return {"level": "critical", "status": disk.get("percent", "Unknown"), "detail": "Project filesystem is critically full."}
        if percent >= 80:
            return {"level": "warning", "status": disk.get("percent", "Unknown"), "detail": "Project filesystem is above warning threshold."}
        return {"level": "ok", "status": disk.get("percent", "Unknown"), "detail": f"Free: {disk.get('free', 'Unknown')}"}

    def _run_wrapper_validation(self) -> dict[str, Any]:
        status = self.management_service.get_status()
        if not status.get("available"):
            return {"level": "critical", "status": "Missing", "detail": status.get("wrapper", "manage.sh not found")}
        if not status.get("executable"):
            return {"level": "critical", "status": "Not executable", "detail": status.get("wrapper", "manage.sh")}
        return {"level": "ok", "status": status.get("version", "Installed"), "detail": f"{status.get('command_count', 0)} actions available."}

    def _run_event_journal_check(self) -> dict[str, Any]:
        summary = self.event_service.get_summary()
        return {"level": "ok", "status": f"{summary.get('total', 0)} events", "detail": "Operational event journal is readable."}

    def _read_state(self) -> dict[str, Any]:
        try:
            if not self.state_path.exists():
                return {"jobs": {}, "history": []}
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except Exception:
            return {"jobs": {}, "history": []}

    def _write_state(self, state: dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(self.state_path)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _format_time(self, value: datetime) -> str:
        return value.isoformat(timespec="seconds")

    def _parse_time(self, value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
