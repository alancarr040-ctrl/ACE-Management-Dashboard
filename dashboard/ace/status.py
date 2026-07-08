from __future__ import annotations

from datetime import datetime
import socket


class ACEStatusService:
    def __init__(self, docker_service, db_host: str = "ace-db", db_port: int = 3306):
        self.docker_service = docker_service
        self.db_host = db_host
        self.db_port = db_port

    def get_status(self) -> dict[str, str]:
        ace = self.docker_service.get_container_by_name("ace-server")
        logs = self.docker_service.get_container_logs("ace-server", lines=80)
        db_tcp = self._check_tcp(self.db_host, self.db_port)

        last_error = self._extract_last_error(logs)
        docker_health = ace.get("health_display", "Unknown") if ace else "Missing"
        container_state = ace.get("state_display", "Missing") if ace else "Missing"

        if ace and ace.get("status") == "running" and ace.get("health_normalized") == "healthy" and db_tcp:
            server_status = "Online"
        elif ace and ace.get("status") == "running":
            server_status = "Degraded"
        else:
            server_status = "Offline"

        return {
            "server_status": server_status,
            "container_state": container_state,
            "docker_health": docker_health,
            "database_tcp": "Connected" if db_tcp else "Failed",
            "database_auth": "Not Tested",
            "ace_process": "Running" if ace and ace.get("status") == "running" else "Not Running",
            "server_uptime": ace.get("uptime", "") if ace else "",
            "players": "Not Integrated",
            "world": "Not Integrated",
            "server_version": "Not Integrated",
            "last_error": last_error or "None",
            "checked_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }

    def _check_tcp(self, host: str, port: int) -> bool:
        try:
            with socket.create_connection((host, port), timeout=3):
                return True
        except OSError:
            return False

    def _extract_last_error(self, logs: str) -> str:
        interesting = [
            "Connect Timeout expired",
            "Unhandled exception",
            "Access denied",
            "Can't connect",
            "ERROR",
            "Exception",
        ]
        for line in reversed(logs.splitlines()):
            if any(token in line for token in interesting):
                return line[-220:]
        return ""
