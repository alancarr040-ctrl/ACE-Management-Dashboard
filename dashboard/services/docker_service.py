from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import docker
from docker.errors import DockerException, NotFound


FRIENDLY = {
    "ace-dashboard": ("ACE Dashboard", "Management Interface"),
    "ace-db": ("ACE Database", "MySQL 8"),
    "ace-server": ("ACE Server", "World Emulator"),
}


class DockerService:
    def __init__(self):
        self.client = docker.from_env()

    def get_containers(self) -> list[dict[str, Any]]:
        try:
            return [self._container_summary(c) for c in self.client.containers.list(all=True)]
        except DockerException as exc:
            return [{"name": "Docker error", "friendly_name": "Docker error", "error": str(exc)}]

    def get_container_by_name(self, name: str) -> dict[str, Any] | None:
        for container in self.get_containers():
            if container.get("name") == name:
                return container
        return None

    def get_summary(self) -> dict[str, int]:
        containers = self.get_containers()
        valid = [c for c in containers if not c.get("error")]
        return {
            "total": len(valid),
            "running": sum(1 for c in valid if c.get("status") == "running"),
            "stopped": sum(1 for c in valid if c.get("status") in ("exited", "created")),
            "healthy": sum(1 for c in valid if c.get("health_normalized") == "healthy"),
            "unhealthy": sum(1 for c in valid if c.get("health_normalized") == "unhealthy"),
            "not_monitored": sum(1 for c in valid if c.get("health_normalized") == "not_monitored"),
            "starting": sum(1 for c in valid if c.get("health_normalized") == "starting"),
        }

    def get_resources(self) -> dict[str, int]:
        try:
            return {
                "containers": len(self.client.containers.list(all=True)),
                "images": len(self.client.images.list()),
                "networks": len(self.client.networks.list()),
                "volumes": len(self.client.volumes.list()),
            }
        except DockerException:
            return {"containers": 0, "images": 0, "networks": 0, "volumes": 0}

    def get_container_logs(self, name: str, lines: int = 100) -> str:
        try:
            lines = max(10, min(int(lines), 500))
            container = self.client.containers.get(name)
            logs = container.logs(tail=lines, timestamps=True)
            return logs.decode("utf-8", errors="replace")
        except NotFound:
            return f"Container not found: {name}"
        except DockerException as exc:
            return f"Docker error: {exc}"

    def restart_container(self, name: str) -> tuple[bool, str]:
        if name != "ace-server":
            return False, f"Restart is currently enabled only for ace-server. Requested: {name}"
        try:
            container = self.client.containers.get(name)
            container.restart(timeout=30)
            return True, f"{name} restarted successfully."
        except DockerException as exc:
            return False, f"Docker restart failed: {exc}"

    def _container_summary(self, c) -> dict[str, Any]:
        attrs = c.attrs or {}
        state = attrs.get("State", {})
        host_config = attrs.get("HostConfig", {})
        network_settings = attrs.get("NetworkSettings", {})

        display, subtitle = FRIENDLY.get(c.name, (c.name, "Docker Container"))
        health = self._health(state)
        created = attrs.get("Created", "")
        started = state.get("StartedAt", "")

        return {
            "name": c.name,
            "friendly_name": display,
            "subtitle": subtitle,
            "image": c.image.tags[0] if c.image.tags else c.image.short_id,
            "container_id": c.short_id,
            "status": c.status,
            "status_display": self._title(c.status),
            "state": state.get("Status", "unknown"),
            "state_display": self._title(state.get("Status", "unknown")),
            "health": health["raw"],
            "health_display": health["display"],
            "health_normalized": health["normalized"],
            "restart_policy": host_config.get("RestartPolicy", {}).get("Name", "none"),
            "restart_count": state.get("RestartCount", 0),
            "created": self._format_timestamp(created),
            "started": self._format_timestamp(started),
            "uptime": self._uptime(started),
            "ports": network_settings.get("Ports", {}) or {},
            "networks": list((network_settings.get("Networks", {}) or {}).keys()),
            "mounts": [
                {"source": m.get("Source", ""), "destination": m.get("Destination", ""), "mode": m.get("Mode", "")}
                for m in attrs.get("Mounts", [])
            ],
            "can_restart": c.name == "ace-server",
            "can_start": False,
            "can_stop": False,
        }

    def _health(self, state: dict[str, Any]) -> dict[str, str]:
        raw = state.get("Health", {}).get("Status")
        if not raw:
            return {"raw": "not configured", "display": "Not Monitored", "normalized": "not_monitored"}
        if raw == "healthy":
            return {"raw": raw, "display": "Healthy", "normalized": "healthy"}
        if raw == "unhealthy":
            return {"raw": raw, "display": "Unhealthy", "normalized": "unhealthy"}
        if raw == "starting":
            return {"raw": raw, "display": "Starting", "normalized": "starting"}
        return {"raw": raw, "display": self._title(raw), "normalized": raw}

    def _format_timestamp(self, value: str) -> str:
        if not value or value.startswith("0001-"):
            return ""
        try:
            trimmed = value
            if "." in trimmed:
                base, _ = trimmed.split(".", 1)
                trimmed = base + "+00:00" if trimmed.endswith("Z") else base
            elif trimmed.endswith("Z"):
                trimmed = trimmed.replace("Z", "+00:00")
            dt = datetime.fromisoformat(trimmed)
            return dt.strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            return value

    def _uptime(self, started: str) -> str:
        if not started or started.startswith("0001-"):
            return ""
        try:
            trimmed = started
            if "." in trimmed:
                base, _ = trimmed.split(".", 1)
                trimmed = base + "+00:00" if trimmed.endswith("Z") else base
            elif trimmed.endswith("Z"):
                trimmed = trimmed.replace("Z", "+00:00")
            dt = datetime.fromisoformat(trimmed)
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

    def _title(self, value: str) -> str:
        return (value or "unknown").replace("_", " ").title()
