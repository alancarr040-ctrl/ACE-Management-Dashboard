from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence


class ManagementService:
    """Controlled integration layer for the ACE Management Utility wrapper.

    The dashboard never accepts arbitrary shell text from the browser.  It exposes
    a small catalog of whitelisted wrapper actions and executes those actions by
    passing an argv list directly to subprocess with shell=False.
    """

    def __init__(self, root_path: str | Path | None = None):
        self.root_path = Path(root_path or os.environ.get("ACE_ROOT", "/opt/acserver")).resolve()
        self.wrapper_path = self.root_path / "manage.sh"
        self.audit_path = Path(os.environ.get("ACE_MANAGEMENT_AUDIT", self.root_path / "backups" / "runtime" / "management-audit.jsonl"))
        self.timeout_seconds = int(os.environ.get("ACE_MANAGEMENT_TIMEOUT", "90"))

    def get_status(self) -> Dict[str, object]:
        groups = self.get_actions()
        return {
            "name": "ACE Management Utility",
            "version": self._read_wrapper_version(),
            "wrapper": str(self.wrapper_path),
            "available": self.wrapper_path.exists(),
            "executable": self.wrapper_path.exists() and self.wrapper_path.stat().st_mode & 0o111 != 0,
            "command_count": sum(len(group["actions"]) for group in groups),
            "groups": groups,
            "mode": "Interactive wrapper integration",
            "safe_mode": "Only whitelisted non-interactive manage.sh actions are exposed. Shell actions remain SSH/manual only.",
            "last_runs": self.get_recent_runs(),
        }

    def get_actions(self) -> List[Dict[str, object]]:
        return [
            {
                "group": "System",
                "actions": [
                    self._action("status", "Status", ["status"], "Show Docker Compose service status.", "Read"),
                    self._action("start", "Start Stack", ["start"], "Start the ACE stack.", "Change", confirm=True, dry_run=True, web_enabled=False, manual_reason="Full-stack actions may interrupt the dashboard session; use Dry Run here and run from SSH for now."),
                    self._action("stop", "Stop Stack", ["stop"], "Stop the ACE stack without removing containers.", "Change", confirm=True, dry_run=True, web_enabled=False, manual_reason="Full-stack actions may interrupt the dashboard session; use Dry Run here and run from SSH for now."),
                    self._action("restart_all", "Restart Stack", ["restart", "all"], "Restart the full ACE stack.", "Change", confirm=True, dry_run=True, web_enabled=False, manual_reason="Full-stack restart may interrupt the dashboard session; use Dry Run here and run from SSH for now."),
                    self._action("rebuild_dashboard", "Rebuild Dashboard", ["rebuild", "dashboard"], "Rebuild and restart only the dashboard service.", "Change", confirm=True, dry_run=True, web_enabled=False, manual_reason="Dashboard rebuild restarts the web container serving this page; use Dry Run here and run from SSH until queued rebuild support exists."),
                ],
            },
            {
                "group": "Dashboard",
                "actions": [
                    self._action("dashboard_logs", "Dashboard Logs", ["dashboard", "logs", "150"], "Show recent dashboard container logs.", "Read"),
                    self._action("dashboard_restart", "Restart Dashboard", ["dashboard", "restart"], "Restart the dashboard container.", "Change", confirm=True, dry_run=True, web_enabled=False, manual_reason="Dashboard restart interrupts the web session; use Dry Run here and run from SSH until reconnect handling exists."),
                    self._action("dashboard_rebuild", "Rebuild Dashboard", ["dashboard", "rebuild"], "Rebuild and restart the dashboard container.", "Change", confirm=True, dry_run=True, web_enabled=False, manual_reason="Dashboard rebuild interrupts the web session; use Dry Run here and run from SSH until queued rebuild support exists."),
                ],
            },
            {
                "group": "Server",
                "actions": [
                    self._action("server_status", "Server Status", ["server", "status"], "Show ACE server container status.", "Read"),
                    self._action("server_logs", "Server Logs", ["server", "logs", "150"], "Show recent ACE server logs.", "Read"),
                    self._action("server_restart", "Restart Server", ["server", "restart"], "Restart the ACE server container.", "Change", confirm=True, dry_run=True),
                ],
            },
            {
                "group": "Database",
                "actions": [
                    self._action("db_status", "Database Status", ["db", "status"], "Show ACE database container status.", "Read"),
                    self._action("db_logs", "Database Logs", ["db", "logs", "150"], "Show recent ACE database logs.", "Read"),
                    self._action("db_restart", "Restart Database", ["db", "restart"], "Restart the ACE database container.", "Change", confirm=True, dry_run=True),
                ],
            },
            {
                "group": "Backups",
                "actions": [
                    self._action("backup_list", "List Backups", ["backup", "list"], "List backup folders.", "Read"),
                    self._action("backup_verify", "Verify Backups", ["backup", "verify"], "Show backup folders and manifest status.", "Read"),
                    self._action("backup_create", "Create Backup", ["backup", "create"], "Run the existing runtime backup script.", "Change", confirm=True, dry_run=True),
                ],
            },
            {
                "group": "Maintenance",
                "actions": [
                    self._action("doctor", "Doctor", ["doctor"], "Run local environment checks.", "Read"),
                    self._action("version", "Version", ["version"], "Show utility and dashboard version metadata.", "Read"),
                    self._action("help", "Help", ["help"], "Show wrapper help.", "Read"),
                ],
            },
        ]

    def run_action(self, action_id: str, *, dry_run: bool = False) -> Dict[str, object]:
        action = self._find_action(action_id)
        if action is None:
            return self._result(action_id, [], 127, "", f"Unknown management action: {action_id}", False)
        if not dry_run and action.get("web_enabled") is False:
            return self._result(
                action_id,
                action["args"],
                65,
                "",
                action.get("manual_reason") or "This action is documented but disabled from the web UI. Run it from SSH/manual control for now.",
                False,
            )
        if not self.wrapper_path.exists():
            return self._result(action_id, action["args"], 127, "", f"Wrapper not found: {self.wrapper_path}", False)
        if not (self.wrapper_path.stat().st_mode & 0o111):
            return self._result(action_id, action["args"], 126, "", f"Wrapper is not executable: {self.wrapper_path}", False)

        args: List[str] = list(action["args"])
        if dry_run:
            if not action.get("dry_run", False):
                return self._result(action_id, args, 64, "", "Dry-run is not supported for this action.", False)
            args = ["--dry-run", *args]

        argv = [str(self.wrapper_path), *args]
        started = datetime.now(timezone.utc)
        try:
            completed = subprocess.run(
                argv,
                cwd=str(self.root_path),
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
                shell=False,
            )
            result = self._result(action_id, args, completed.returncode, completed.stdout, completed.stderr, completed.returncode == 0)
        except subprocess.TimeoutExpired as exc:
            result = self._result(
                action_id,
                args,
                124,
                exc.stdout or "",
                f"Command timed out after {self.timeout_seconds} seconds.",
                False,
            )
        except OSError as exc:
            result = self._result(action_id, args, getattr(exc, "errno", 1) or 1, "", str(exc), False)
        result["started_at"] = started.isoformat()
        result["finished_at"] = datetime.now(timezone.utc).isoformat()
        result["label"] = action["label"]
        result["dry_run"] = dry_run
        self._record_run(result)
        return result

    def get_recent_runs(self, limit: int = 10) -> List[Dict[str, object]]:
        if not self.audit_path.exists():
            return []
        try:
            lines = self.audit_path.read_text(encoding="utf-8").splitlines()[-limit:]
            rows = [json.loads(line) for line in lines if line.strip()]
            return list(reversed(rows))
        except Exception:
            return []

    def _action(self, action_id: str, label: str, args: Sequence[str], description: str, action_type: str, *, confirm: bool = False, dry_run: bool = False, web_enabled: bool = True, manual_reason: str = "") -> Dict[str, object]:
        return {
            "id": action_id,
            "label": label,
            "args": list(args),
            "command": "./manage.sh " + " ".join(args),
            "description": description,
            "type": action_type,
            "confirm": confirm,
            "dry_run": dry_run,
            "web_enabled": web_enabled,
            "manual_reason": manual_reason,
        }

    def _find_action(self, action_id: str) -> Dict[str, object] | None:
        for group in self.get_actions():
            for action in group["actions"]:
                if action["id"] == action_id:
                    return action
        return None

    def _read_wrapper_version(self) -> str:
        if not self.wrapper_path.exists():
            return "Not installed"
        try:
            for line in self.wrapper_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.startswith("ACE_MANAGE_VERSION="):
                    return line.split("=", 1)[1].strip().strip('"')
        except Exception:
            pass
        return "Unknown"

    def _result(self, action_id: str, args: Sequence[str], exit_code: int, stdout: str, stderr: str, success: bool) -> Dict[str, object]:
        return {
            "action_id": action_id,
            "command": "./manage.sh " + " ".join(args),
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "success": success,
        }

    def _record_run(self, result: Dict[str, object]) -> None:
        try:
            self.audit_path.parent.mkdir(parents=True, exist_ok=True)
            record = {
                "timestamp": result.get("finished_at"),
                "action_id": result.get("action_id"),
                "label": result.get("label"),
                "command": result.get("command"),
                "exit_code": result.get("exit_code"),
                "success": result.get("success"),
                "dry_run": result.get("dry_run", False),
            }
            with self.audit_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        except Exception:
            # The action result is more important than audit persistence.  Avoid
            # failing the management request if the audit path is unavailable.
            return
