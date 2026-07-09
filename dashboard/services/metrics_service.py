from __future__ import annotations

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from docker.errors import DockerException, NotFound

from services.docker_service import FRIENDLY
from utils.status import severity_badge_class
from utils.time_format import time_display


class MetricsService:
    """Read-only ACEMD metrics aggregation.

    Phase 2.8.0 intentionally keeps metrics lightweight and operational.  The
    service does not try to replace Prometheus/Grafana; it provides the compact
    measurements ACEMD pages need for status, thresholds, and future alerts.
    """

    def __init__(self, docker_service, system_service, backup_service, management_service, event_service, root_path: str | Path | None = None):
        self.docker_service = docker_service
        self.system_service = system_service
        self.backup_service = backup_service
        self.management_service = management_service
        self.event_service = event_service
        self.root_path = Path(root_path or os.environ.get("ACE_ROOT", "/opt/acserver")).resolve()
        self.automation_service = None

    def bind_automation(self, automation_service) -> None:
        self.automation_service = automation_service

    def get_metrics(self) -> dict[str, Any]:
        generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        system = self._system_metrics()
        storage = self._storage_metrics()
        containers = self._docker_container_metrics()
        docker_summary = self._docker_summary(containers)
        database = self._database_metrics(containers)
        acemd = self._acemd_metrics()

        checks = self._threshold_checks(system, storage, containers, database)
        overall = self._overall(checks)

        return {
            "generated_at": generated_at,
            "generated_display": time_display(generated_at),
            "overall": overall,
            "summary": {
                "cpu": system["cpu"]["percent"],
                "memory": system["memory"]["percent"],
                "disk": storage["project"]["percent"],
                "containers": f"{docker_summary['running']}/{docker_summary['total']}",
                "warnings": sum(1 for c in checks if c["level"] == "warning"),
                "critical": sum(1 for c in checks if c["level"] == "critical"),
            },
            "system": system,
            "storage": storage,
            "docker": docker_summary,
            "containers": containers,
            "database": database,
            "acemd": acemd,
            "checks": checks,
            "thresholds": self._thresholds(),
        }

    def _system_metrics(self) -> dict[str, Any]:
        cpu_count = os.cpu_count() or 1
        try:
            load1, load5, load15 = os.getloadavg()
            cpu_percent = min(999.0, (load1 / cpu_count) * 100.0)
        except (OSError, AttributeError):
            load1 = load5 = load15 = 0.0
            cpu_percent = 0.0
        memory = self._memory_metrics()
        return {
            "cpu": {
                "label": "CPU Load",
                "percent": self._percent(cpu_percent),
                "raw_percent": round(cpu_percent, 1),
                "cores": cpu_count,
                "load1": round(load1, 2),
                "load5": round(load5, 2),
                "load15": round(load15, 2),
                "level": self._level(cpu_percent, 70, 90),
                "badge": severity_badge_class(self._level(cpu_percent, 70, 90)),
            },
            "memory": memory,
        }

    def _memory_metrics(self) -> dict[str, Any]:
        meminfo = self._read_meminfo()
        total = meminfo.get("MemTotal", 0) * 1024
        available = meminfo.get("MemAvailable", 0) * 1024
        free = meminfo.get("MemFree", 0) * 1024
        cached = (meminfo.get("Cached", 0) + meminfo.get("SReclaimable", 0)) * 1024
        swap_total = meminfo.get("SwapTotal", 0) * 1024
        swap_free = meminfo.get("SwapFree", 0) * 1024
        used = max(0, total - available)
        pct = (used / total * 100) if total else 0.0
        swap_used = max(0, swap_total - swap_free)
        swap_pct = (swap_used / swap_total * 100) if swap_total else 0.0
        level = self._level(pct, 75, 90)
        return {
            "label": "Memory",
            "total": self._bytes(total),
            "used": self._bytes(used),
            "available": self._bytes(available),
            "free": self._bytes(free),
            "cached": self._bytes(cached),
            "swap_used": self._bytes(swap_used),
            "swap_total": self._bytes(swap_total),
            "swap_percent": self._percent(swap_pct),
            "percent": self._percent(pct),
            "raw_percent": round(pct, 1),
            "level": level,
            "badge": severity_badge_class(level),
        }

    def _storage_metrics(self) -> dict[str, Any]:
        project = self._disk_for_path(self.root_path, "Project Filesystem")
        backup_path = self.root_path / "backups"
        backups = self._disk_for_path(backup_path if backup_path.exists() else self.root_path, "Backups")
        return {"project": project, "backups": backups}

    def _disk_for_path(self, path: Path, label: str) -> dict[str, Any]:
        try:
            usage = shutil.disk_usage(path)
            pct = (usage.used / usage.total * 100) if usage.total else 0.0
            level = self._level(pct, 80, 90)
            return {
                "label": label,
                "path": str(path),
                "total": self._bytes(usage.total),
                "used": self._bytes(usage.used),
                "free": self._bytes(usage.free),
                "percent": self._percent(pct),
                "raw_percent": round(pct, 1),
                "level": level,
                "badge": severity_badge_class(level),
            }
        except Exception as exc:
            return {"label": label, "path": str(path), "total": "Unknown", "used": "Unknown", "free": "Unknown", "percent": "Unknown", "raw_percent": 0, "level": "unknown", "badge": "gray", "error": str(exc)}

    def _docker_container_metrics(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        try:
            containers = self.docker_service.client.containers.list(all=True)
        except DockerException as exc:
            return [{"name": "Docker", "friendly_name": "Docker", "status": "Unavailable", "level": "critical", "error": str(exc), "cpu_percent": "Unknown", "memory_percent": "Unknown", "memory_used": "Unknown", "memory_limit": "Unknown", "network_rx": "Unknown", "network_tx": "Unknown", "restarts": 0, "uptime": ""}]

        for container in containers:
            try:
                attrs = container.attrs or {}
                state = attrs.get("State", {})
                display, subtitle = self._friendly(container.name)
                stats = self._container_stats(container) if container.status == "running" else {}
                mem_pct = stats.get("memory_raw_percent", 0.0)
                cpu_pct = stats.get("cpu_raw_percent", 0.0)
                level = "ok"
                health = state.get("Health", {}).get("Status") or "not monitored"
                if container.status != "running" or health == "unhealthy":
                    level = "critical"
                elif health == "starting" or mem_pct >= 85 or cpu_pct >= 90:
                    level = "warning"
                rows.append({
                    "name": container.name,
                    "friendly_name": display,
                    "subtitle": subtitle,
                    "status": container.status.title(),
                    "health": health.replace("_", " ").title(),
                    "level": level,
                    "badge": severity_badge_class(level),
                    "cpu_percent": stats.get("cpu_percent", "0.0%" if container.status == "running" else "Stopped"),
                    "cpu_raw_percent": cpu_pct,
                    "memory_percent": stats.get("memory_percent", "0.0%" if container.status == "running" else "Stopped"),
                    "memory_raw_percent": mem_pct,
                    "memory_used": stats.get("memory_used", "0 B"),
                    "memory_limit": stats.get("memory_limit", "0 B"),
                    "network_rx": stats.get("network_rx", "0 B"),
                    "network_tx": stats.get("network_tx", "0 B"),
                    "restarts": state.get("RestartCount", 0),
                    "uptime": self._uptime(state.get("StartedAt", "")),
                })
            except Exception as exc:
                rows.append({"name": getattr(container, "name", "unknown"), "friendly_name": getattr(container, "name", "unknown"), "status": "Error", "level": "warning", "badge": "yellow", "error": str(exc), "cpu_percent": "Unknown", "memory_percent": "Unknown", "memory_used": "Unknown", "memory_limit": "Unknown", "network_rx": "Unknown", "network_tx": "Unknown", "restarts": 0, "uptime": ""})
        return sorted(rows, key=lambda row: row.get("name", ""))

    def _container_stats(self, container) -> dict[str, Any]:
        try:
            stats = container.stats(stream=False)
        except (DockerException, NotFound):
            return {}
        cpu_pct = self._docker_cpu_percent(stats)
        mem = stats.get("memory_stats", {}) or {}
        usage = int(mem.get("usage", 0) or 0)
        stats_mem = mem.get("stats", {}) or {}
        cache = int(stats_mem.get("cache", 0) or 0)
        used = max(0, usage - cache)
        limit = int(mem.get("limit", 0) or 0)
        mem_pct = (used / limit * 100) if limit else 0.0
        net_rx = net_tx = 0
        for iface in (stats.get("networks", {}) or {}).values():
            net_rx += int(iface.get("rx_bytes", 0) or 0)
            net_tx += int(iface.get("tx_bytes", 0) or 0)
        return {
            "cpu_percent": self._percent(cpu_pct),
            "cpu_raw_percent": round(cpu_pct, 1),
            "memory_percent": self._percent(mem_pct),
            "memory_raw_percent": round(mem_pct, 1),
            "memory_used": self._bytes(used),
            "memory_limit": self._bytes(limit),
            "network_rx": self._bytes(net_rx),
            "network_tx": self._bytes(net_tx),
        }

    def _docker_cpu_percent(self, stats: dict[str, Any]) -> float:
        cpu_stats = stats.get("cpu_stats", {}) or {}
        precpu_stats = stats.get("precpu_stats", {}) or {}
        cpu_usage = (cpu_stats.get("cpu_usage", {}) or {}).get("total_usage", 0) or 0
        precpu_usage = (precpu_stats.get("cpu_usage", {}) or {}).get("total_usage", 0) or 0
        system_usage = cpu_stats.get("system_cpu_usage", 0) or 0
        presystem_usage = precpu_stats.get("system_cpu_usage", 0) or 0
        cpu_delta = cpu_usage - precpu_usage
        system_delta = system_usage - presystem_usage
        online_cpus = cpu_stats.get("online_cpus") or len((cpu_stats.get("cpu_usage", {}) or {}).get("percpu_usage", []) or []) or 1
        if cpu_delta > 0 and system_delta > 0:
            return (cpu_delta / system_delta) * online_cpus * 100.0
        return 0.0

    def _docker_summary(self, containers: list[dict[str, Any]]) -> dict[str, Any]:
        total = len([c for c in containers if not c.get("error")])
        running = sum(1 for c in containers if c.get("status") == "Running")
        cpu_total = sum(float(c.get("cpu_raw_percent") or 0) for c in containers)
        memory_total = sum(float(c.get("memory_raw_percent") or 0) for c in containers)
        critical = sum(1 for c in containers if c.get("level") == "critical")
        warning = sum(1 for c in containers if c.get("level") == "warning")
        level = "critical" if critical else "warning" if warning else "ok"
        return {
            "total": total,
            "running": running,
            "cpu_total": self._percent(cpu_total),
            "memory_average": self._percent(memory_total / total if total else 0),
            "critical": critical,
            "warning": warning,
            "level": level,
            "badge": severity_badge_class(level),
        }

    def _database_metrics(self, containers: list[dict[str, Any]]) -> dict[str, Any]:
        db = next((c for c in containers if c.get("name") == "ace-db"), None)
        if not db:
            return {"status": "Missing", "level": "critical", "badge": "red", "cpu_percent": "Unknown", "memory_percent": "Unknown", "connections": "Not connected", "queries": "Not connected", "uptime": ""}
        level = db.get("level", "unknown")
        return {
            "status": db.get("status", "Unknown"),
            "health": db.get("health", "Unknown"),
            "level": level,
            "badge": severity_badge_class(level),
            "cpu_percent": db.get("cpu_percent", "Unknown"),
            "memory_percent": db.get("memory_percent", "Unknown"),
            "memory_used": db.get("memory_used", "Unknown"),
            "restarts": db.get("restarts", 0),
            "uptime": db.get("uptime", ""),
            "connections": "Deferred",
            "queries": "Deferred",
            "detail": "Container-level database metrics are available. SQL-level metrics are reserved for the ACE data integration phase.",
        }

    def _acemd_metrics(self) -> dict[str, Any]:
        management = self._safe(self.management_service.get_status, {})
        events = self._safe(self.event_service.get_summary, {})
        automation = self._safe(lambda: self.automation_service.get_status(run_due=False) if self.automation_service else {}, {})
        jobs = (automation.get("engine", {}) if isinstance(automation, dict) else {}).get("jobs", 0)
        failures = (automation.get("engine", {}) if isinstance(automation, dict) else {}).get("failures", 0)
        level = "warning" if failures else "ok"
        return {
            "wrapper_version": management.get("version", "Unknown") if isinstance(management, dict) else "Unknown",
            "wrapper_actions": management.get("command_count", 0) if isinstance(management, dict) else 0,
            "automation_jobs": jobs,
            "automation_failures": failures,
            "events_total": events.get("total", 0) if isinstance(events, dict) else 0,
            "events_warning": events.get("warning", 0) if isinstance(events, dict) else 0,
            "events_critical": events.get("critical", 0) if isinstance(events, dict) else 0,
            "level": level,
            "badge": severity_badge_class(level),
        }

    def _threshold_checks(self, system: dict[str, Any], storage: dict[str, Any], containers: list[dict[str, Any]], database: dict[str, Any]) -> list[dict[str, Any]]:
        checks = [
            self._check("CPU load", system["cpu"]["level"], system["cpu"]["percent"], f"1m load {system['cpu']['load1']} across {system['cpu']['cores']} cores."),
            self._check("Memory usage", system["memory"]["level"], system["memory"]["percent"], f"Available: {system['memory']['available']}"),
            self._check("Project disk", storage["project"]["level"], storage["project"]["percent"], f"Free: {storage['project']['free']}"),
            self._check("Backup disk", storage["backups"]["level"], storage["backups"]["percent"], f"Free: {storage['backups']['free']}"),
        ]
        critical_containers = [c for c in containers if c.get("level") == "critical"]
        warning_containers = [c for c in containers if c.get("level") == "warning"]
        if critical_containers:
            checks.append(self._check("Container resources", "critical", f"{len(critical_containers)} critical", "One or more required containers are stopped or unhealthy."))
        elif warning_containers:
            checks.append(self._check("Container resources", "warning", f"{len(warning_containers)} warning", "One or more containers are starting or near a resource threshold."))
        else:
            checks.append(self._check("Container resources", "ok", "OK", "Container resource metrics are within operational thresholds."))
        checks.append(self._check("Database container", database.get("level", "unknown"), database.get("status", "Unknown"), database.get("detail", database.get("health", ""))))
        return checks

    def _overall(self, checks: list[dict[str, Any]]) -> dict[str, str]:
        if any(c["level"] == "critical" for c in checks):
            return {"level": "critical", "label": "Critical", "message": "One or more resource checks need immediate attention.", "badge": "red"}
        if any(c["level"] == "warning" for c in checks):
            return {"level": "warning", "label": "Warning", "message": "Resource monitoring is operating with warnings.", "badge": "yellow"}
        return {"level": "ok", "label": "Nominal", "message": "Core ACEMD resource metrics are within operational thresholds.", "badge": "green"}

    def _thresholds(self) -> dict[str, str]:
        return {"cpu_warning": "70%", "cpu_critical": "90%", "memory_warning": "75%", "memory_critical": "90%", "disk_warning": "80%", "disk_critical": "90%"}

    def _check(self, name: str, level: str, status: str, detail: str) -> dict[str, str]:
        return {"name": name, "level": level, "status": status, "detail": detail, "badge": severity_badge_class(level)}

    def _read_meminfo(self) -> dict[str, int]:
        data: dict[str, int] = {}
        try:
            for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
                if not line or ":" not in line:
                    continue
                key, rest = line.split(":", 1)
                value = rest.strip().split()[0]
                data[key] = int(value)
        except Exception:
            pass
        return data

    def _safe(self, fn, fallback):
        try:
            return fn()
        except Exception:
            return fallback

    def _level(self, value: float, warning: float, critical: float) -> str:
        if value >= critical:
            return "critical"
        if value >= warning:
            return "warning"
        return "ok"

    def _percent(self, value: float) -> str:
        return f"{round(float(value), 1)}%"

    def _bytes(self, value: int | float) -> str:
        value = float(value or 0)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024:
                return f"{value:.1f} {unit}"
            value /= 1024
        return f"{value:.1f} PB"

    def _friendly(self, name: str) -> tuple[str, str]:
        return FRIENDLY.get(name, (name, "Docker Container"))

    def _uptime(self, started: str) -> str:
        if not started or started.startswith("0001-"):
            return ""
        try:
            text = started
            if "." in text:
                base, _ = text.split(".", 1)
                text = base + "+00:00" if text.endswith("Z") else base
            elif text.endswith("Z"):
                text = text.replace("Z", "+00:00")
            dt = datetime.fromisoformat(text)
            delta = datetime.now(timezone.utc) - dt.astimezone(timezone.utc)
            minutes = max(0, int(delta.total_seconds() // 60))
            days, rem = divmod(minutes, 1440)
            hours, mins = divmod(rem, 60)
            if days:
                return f"{days}d {hours}h"
            if hours:
                return f"{hours}h {mins}m"
            return f"{mins}m"
        except Exception:
            return ""
