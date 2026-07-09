from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from services.automation_jobs import AutomationJob, AutomationJobRegistry
from utils.time_format import time_display
from utils.status import severity_badge_class


class AutomationService:
    """Request-driven ACEMD automation scheduler.

    Phase 2.7.2 introduces a small job registry so built-in jobs are registered as
    scheduler objects instead of being embedded directly in the scheduler loop.  The
    engine remains request-driven and read-only; it does not create cron entries or a
    host daemon.
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
        self.registry = AutomationJobRegistry()
        self._register_builtin_jobs()

    @property
    def jobs(self) -> list[AutomationJob]:
        return self.registry.all()

    def get_status(self, run_due: bool = True) -> dict[str, Any]:
        if run_due:
            self.run_due_jobs()
        state = self._read_state()
        jobs = [self._job_view(job, state) for job in self.jobs]
        enabled = sum(1 for j in jobs if j["enabled"])
        disabled = len(jobs) - enabled
        last_runs = [j for j in jobs if j.get("last_run_raw")]
        last_run_raw = max((j["last_run_raw"] for j in last_runs), default=None)
        next_due_candidates = [j["next_run_raw"] for j in jobs if j.get("enabled") and j.get("next_run_raw")]
        next_run_raw = min(next_due_candidates) if next_due_candidates else None
        failures = sum(1 for j in jobs if j.get("last_result_level") in ("warning", "critical"))
        history = [self._history_view(row) for row in list(reversed(state.get("history", [])[-self.max_history:]))]
        return {
            "engine": {
                "status": "Running",
                "mode": "Request-driven",
                "registry": "Built-in registry",
                "jobs": len(jobs),
                "enabled": enabled,
                "disabled": disabled,
                "last_tick": state.get("last_tick", "Never"),
                "last_tick_display": time_display(state.get("last_tick")),
                "last_run": last_run_raw or "Never",
                "last_run_display": time_display(last_run_raw),
                "next_run": next_run_raw or "None",
                "next_run_display": time_display(next_run_raw, future=True),
                "failures": failures,
                "groups": len(self.registry.groups()),
            },
            "jobs": jobs,
            "history": history,
        }

    def run_due_jobs(self) -> list[dict[str, Any]]:
        now = self._now()
        state = self._read_state()
        state["last_tick"] = self._format_time(now)
        results = []
        for job in self.jobs:
            if not job.enabled:
                continue
            current = state.setdefault("jobs", {}).setdefault(job.id, {})
            next_run = self._parse_time(current.get("next_run"))
            if next_run is None or now >= next_run:
                results.append(self.run_job(job.id, state=state, manual=False))
        self._write_state(state)
        return results

    def run_job(self, job_id: str, state: dict[str, Any] | None = None, manual: bool = True) -> dict[str, Any]:
        job = self.registry.get(job_id)
        if not job:
            return {"job_id": job_id, "success": False, "level": "critical", "message": "Unknown job."}
        own_state = state is None
        if state is None:
            state = self._read_state()
        now = self._now()
        job_state = state.setdefault("jobs", {}).setdefault(job_id, {})
        try:
            result = job.runner()
            success = result.get("level") not in ("critical", "warning")
        except Exception as exc:
            result = {"level": "critical", "status": "Failed", "detail": str(exc)}
            success = False
        next_run = now + timedelta(seconds=int(job.interval_seconds))
        history_row = {
            "timestamp": self._format_time(now),
            "job_id": job_id,
            "job_name": job.name,
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
        if job.produces_events:
            self.event_service.record_event(
                source="automation",
                event_type="automation_job_completed",
                severity="warning" if history_row["level"] == "warning" else "critical" if history_row["level"] == "critical" else "info",
                title=f"Automation job {'manual run' if manual else 'completed'}",
                message=f"{job.name}: {history_row['status']}. {history_row['detail']}",
                entity=job.name,
                current=history_row["status"],
                metadata={"job_id": job_id, "manual": manual, "group": job.group, "category": job.category},
            )
        if own_state:
            state["last_tick"] = self._format_time(now)
            self._write_state(state)
        return self._history_view(history_row)

    def _register_builtin_jobs(self) -> None:
        self.registry.register(AutomationJob("health_monitor", "Health Monitor", "Core", "Every 30 seconds", 30, "Runs the read-only ACEMD health aggregation and records health transitions.", self._run_health_monitor, category="Health", dependencies=("health_service", "event_service")))
        self.registry.register(AutomationJob("backup_verification", "Backup Verification", "Backups", "Hourly", 3600, "Verifies that ACEMD can see current backup inventory and backup status.", self._run_backup_verification, category="Backups", dependencies=("backup_service",)))
        self.registry.register(AutomationJob("disk_usage_check", "Disk Usage Check", "System", "Every 5 minutes", 300, "Checks project filesystem usage against operational thresholds.", self._run_disk_check, category="System", dependencies=("system_service",)))
        self.registry.register(AutomationJob("wrapper_validation", "Wrapper Validation", "Management", "Every 5 minutes", 300, "Verifies that the management wrapper is installed and executable.", self._run_wrapper_validation, category="Management", dependencies=("management_service",)))
        self.registry.register(AutomationJob("event_journal_check", "Event Journal Check", "Events", "Hourly", 3600, "Verifies that the operational event journal is readable and retaining events.", self._run_event_journal_check, category="Events", dependencies=("event_service",)))

    def _job_view(self, job: AutomationJob, state: dict[str, Any]) -> dict[str, Any]:
        row = state.get("jobs", {}).get(job.id, {})
        last_run = row.get("last_run")
        next_run = row.get("next_run")
        view = job.as_dict()
        view.update({
            "last_run": last_run or "Never",
            "next_run": next_run or "Pending",
            "last_run_raw": last_run,
            "next_run_raw": next_run,
            "last_run_display": time_display(last_run),
            "next_run_display": time_display(next_run, future=True),
            "last_result": row.get("last_result", "Not run"),
            "last_result_level": row.get("last_result_level", "unknown"),
            "last_result_badge": severity_badge_class(row.get("last_result_level")),
            "last_detail": row.get("last_detail", ""),
            "dependency_label": ", ".join(job.dependencies) if job.dependencies else "None",
        })
        return view

    def _history_view(self, row: dict[str, Any]) -> dict[str, Any]:
        ts = row.get("timestamp")
        out = dict(row)
        out["timestamp_display"] = time_display(ts)
        out["level_badge"] = severity_badge_class(row.get("level"))
        return out

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
