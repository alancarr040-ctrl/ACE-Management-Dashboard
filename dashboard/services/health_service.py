from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class HealthService:
    """Read-only operational health aggregation for the ACE dashboard.

    This service intentionally reuses existing dashboard service layers instead of
    executing write-capable management actions.  Every check is defensive: a
    failed check becomes a warning/critical row in the Health page rather than an
    uncaught exception that can take down the route.
    """

    def __init__(self, docker_service, backup_service, system_service, management_service):
        self.docker_service = docker_service
        self.backup_service = backup_service
        self.system_service = system_service
        self.management_service = management_service

    def get_health(self) -> dict[str, Any]:
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        checks: list[dict[str, Any]] = []

        containers = self._safe("Docker containers", self.docker_service.get_containers, [])
        docker_summary = self._safe("Docker summary", self.docker_service.get_summary, {})
        disk = self._safe("Disk usage", self.system_service.get_disk_usage, {})
        backups = self._safe("Backups", self.backup_service.list_backups, [])
        backup_summary = self._safe("Backup summary", self.backup_service.get_summary, {})
        management = self._safe("Management wrapper", self.management_service.get_status, {})

        checks.extend(self._container_checks(containers))
        checks.append(self._disk_check(disk))
        checks.append(self._backup_check(backups, backup_summary))
        checks.append(self._wrapper_check(management))
        checks.extend(self._recent_failure_checks(management))

        overall = self._overall_status(checks)
        services = self._service_rows(containers)
        recent_failures = [r for r in management.get("last_runs", []) if not r.get("success")][:5] if isinstance(management, dict) else []

        return {
            "generated_at": generated_at,
            "overall": overall,
            "summary": {
                "status": overall["label"],
                "level": overall["level"],
                "checks": len(checks),
                "critical": sum(1 for c in checks if c["level"] == "critical"),
                "warning": sum(1 for c in checks if c["level"] == "warning"),
                "ok": sum(1 for c in checks if c["level"] == "ok"),
                "containers": docker_summary.get("total", len(services)) if isinstance(docker_summary, dict) else len(services),
                "running": docker_summary.get("running", 0) if isinstance(docker_summary, dict) else 0,
                "healthy": docker_summary.get("healthy", 0) if isinstance(docker_summary, dict) else 0,
                "recent_failures": len(recent_failures),
            },
            "services": services,
            "checks": checks,
            "disk": disk if isinstance(disk, dict) else {},
            "backup": self._backup_summary(backups, backup_summary),
            "wrapper": self._wrapper_summary(management),
            "recent_failures": recent_failures,
        }

    def _safe(self, label: str, fn, fallback):
        try:
            return fn()
        except Exception as exc:
            return fallback

    def _container_checks(self, containers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not containers:
            return [self._check("Docker", "critical", "No containers returned by Docker.", "Docker may be unavailable to the dashboard container.")]
        if any(c.get("error") for c in containers):
            error = next((c.get("error") for c in containers if c.get("error")), "Docker error")
            return [self._check("Docker", "critical", "Docker query failed.", str(error))]

        checks = []
        required = {
            "ace-dashboard": "Dashboard container",
            "ace-server": "ACE server container",
            "ace-db": "Database container",
        }
        by_name = {c.get("name"): c for c in containers}
        for name, label in required.items():
            c = by_name.get(name)
            if not c:
                checks.append(self._check(label, "critical", "Missing", f"Required container not found: {name}"))
                continue
            if c.get("status") != "running":
                checks.append(self._check(label, "critical", c.get("status_display") or "Not running", f"{name} is not running."))
                continue
            health = c.get("health_normalized")
            if health == "unhealthy":
                checks.append(self._check(label, "critical", "Unhealthy", f"{name} reports Docker health as unhealthy."))
            elif health == "starting":
                checks.append(self._check(label, "warning", "Starting", f"{name} is running but still starting."))
            else:
                detail = c.get("health_display") or c.get("state_display") or "Running"
                checks.append(self._check(label, "ok", detail, f"{name} is running."))
        return checks

    def _service_rows(self, containers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        wanted = ["ace-dashboard", "ace-server", "ace-db"]
        rows = []
        by_name = {c.get("name"): c for c in containers if isinstance(c, dict)}
        for name in wanted:
            c = by_name.get(name)
            if not c:
                rows.append({"name": name, "label": name, "role": "Required", "state": "Missing", "health": "Missing", "uptime": "", "level": "critical"})
                continue
            level = "ok"
            if c.get("status") != "running" or c.get("health_normalized") == "unhealthy":
                level = "critical"
            elif c.get("health_normalized") == "starting":
                level = "warning"
            rows.append({
                "name": name,
                "label": c.get("friendly_name", name),
                "role": c.get("subtitle", "Docker Container"),
                "state": c.get("state_display") or c.get("status_display") or c.get("status") or "Unknown",
                "health": c.get("health_display") or "Not Monitored",
                "uptime": c.get("uptime") or "",
                "image": c.get("image") or "",
                "level": level,
            })
        return rows

    def _disk_check(self, disk: dict[str, Any]) -> dict[str, Any]:
        percent_text = str(disk.get("percent", "0%")).strip().replace("%", "") if isinstance(disk, dict) else "0"
        try:
            percent = float(percent_text)
        except ValueError:
            percent = 0.0
        if percent >= 90:
            return self._check("Disk usage", "critical", disk.get("percent", "Unknown"), "Project filesystem is critically full.")
        if percent >= 80:
            return self._check("Disk usage", "warning", disk.get("percent", "Unknown"), "Project filesystem is above the warning threshold.")
        return self._check("Disk usage", "ok", disk.get("percent", "Unknown"), f"Free: {disk.get('free', 'Unknown')}")

    def _backup_check(self, backups: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, Any]:
        if not backups:
            return self._check("Backups", "warning", "No backups found", "No runtime or baseline backups were discovered.")
        failed = int(summary.get("failed", 0) or 0) + int(summary.get("invalid", 0) or 0) if isinstance(summary, dict) else 0
        latest = backups[0]
        if failed:
            return self._check("Backups", "warning", f"{failed} failed/invalid", f"Latest backup: {latest.get('display_name', latest.get('name', 'Unknown'))}")
        return self._check("Backups", "ok", latest.get("age", "Available"), f"Latest backup: {latest.get('display_name', latest.get('name', 'Unknown'))}")

    def _backup_summary(self, backups: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, Any]:
        latest = backups[0] if backups else None
        return {
            "latest": latest.get("display_name") if latest else "None",
            "latest_age": latest.get("age") if latest else "",
            "latest_status": latest.get("status") if latest else "Missing",
            "total": summary.get("total", 0) if isinstance(summary, dict) else 0,
            "verified": summary.get("verified", 0) if isinstance(summary, dict) else 0,
            "failed": summary.get("failed", 0) if isinstance(summary, dict) else 0,
            "invalid": summary.get("invalid", 0) if isinstance(summary, dict) else 0,
        }

    def _wrapper_check(self, management: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(management, dict):
            return self._check("Management wrapper", "critical", "Unavailable", "Wrapper status could not be read.")
        if not management.get("available"):
            return self._check("Management wrapper", "critical", "Missing", management.get("wrapper", "manage.sh not found"))
        if not management.get("executable"):
            return self._check("Management wrapper", "critical", "Not executable", management.get("wrapper", "manage.sh"))
        return self._check("Management wrapper", "ok", management.get("version", "Installed"), management.get("wrapper", "manage.sh"))

    def _wrapper_summary(self, management: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(management, dict):
            return {"available": False, "executable": False, "version": "Unknown", "actions": 0}
        return {
            "available": bool(management.get("available")),
            "executable": bool(management.get("executable")),
            "version": management.get("version", "Unknown"),
            "actions": management.get("command_count", 0),
        }

    def _recent_failure_checks(self, management: dict[str, Any]) -> list[dict[str, Any]]:
        if not isinstance(management, dict):
            return []
        failures = [r for r in management.get("last_runs", []) if not r.get("success")]
        if not failures:
            return [self._check("Recent command errors", "ok", "None", "No failed management commands in recent activity.")]
        return [self._check("Recent command errors", "warning", str(len(failures)), "One or more recent management commands exited unsuccessfully.")]

    def _overall_status(self, checks: list[dict[str, Any]]) -> dict[str, str]:
        if any(c["level"] == "critical" for c in checks):
            return {"level": "critical", "label": "Critical", "message": "One or more required services or checks need attention."}
        if any(c["level"] == "warning" for c in checks):
            return {"level": "warning", "label": "Warning", "message": "The ACE stack is operating with warnings."}
        return {"level": "ok", "label": "Healthy", "message": "Core ACE services and operational checks look good."}

    def _check(self, name: str, level: str, status: str, detail: str) -> dict[str, str]:
        return {"name": name, "level": level, "status": status, "detail": detail}
