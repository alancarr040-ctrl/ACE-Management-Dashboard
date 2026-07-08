from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import re
import subprocess


@dataclass
class ActionResult:
    ok: bool
    message: str
    output: str = ""
    backup_name: str | None = None


class BackupService:
    def __init__(self, backup_dir: str | Path = "/opt/acserver/backups", backup_script: str | Path = "/opt/acserver/scripts/backup.sh"):
        self.backup_dir = Path(backup_dir)
        self.backup_script = Path(backup_script)

    def create_runtime_backup(self) -> ActionResult:
        started = datetime.now(timezone.utc)
        try:
            proc = subprocess.run([str(self.backup_script)], cwd="/opt/acserver", capture_output=True, text=True, timeout=900, check=False)
        except FileNotFoundError:
            return ActionResult(False, f"Backup script not found: {self.backup_script}")
        except subprocess.TimeoutExpired as exc:
            return ActionResult(False, "Runtime backup timed out.", output=(exc.stdout or "") + (exc.stderr or ""))

        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        backup_name = self._extract_backup_name(output)

        if proc.returncode == 0:
            return ActionResult(True, self._summarize_success(output, backup_name), output, backup_name)

        self._mark_failed_backup(backup_name, proc.returncode, output, started)
        return ActionResult(False, self._summarize_failure(proc.returncode, output, backup_name), output, backup_name)

    def list_backups(self) -> list[dict[str, Any]]:
        if not self.backup_dir.exists():
            return []
        backups = []
        for folder in sorted(self.backup_dir.rglob("*"), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
            if folder.is_dir() and folder.parent != self.backup_dir:
                files = [p for p in folder.iterdir() if p.is_file()]
                if files:
                    backups.append(self._describe_backup(folder, files))
        return backups

    def get_summary(self) -> dict[str, Any]:
        backups = self.list_backups()
        return {
            "total": len(backups),
            "runtime": sum(1 for b in backups if b["type"] == "Runtime"),
            "baseline": sum(1 for b in backups if b["type"] == "Baseline"),
            "verified": sum(1 for b in backups if b["status"] == "Verified"),
            "partial": sum(1 for b in backups if b["status"] == "Partial"),
            "failed": sum(1 for b in backups if b["status"] == "Failed"),
            "invalid": sum(1 for b in backups if b["status"] == "Invalid"),
        }

    def get_storage_summary(self) -> dict[str, Any]:
        backups = self.list_backups()
        total_size = sum(b["total_size_bytes"] for b in backups)
        latest = backups[0] if backups else None
        return {
            "total_size": self._format_bytes(total_size),
            "with_manifest": sum(1 for b in backups if b["has_manifest"]),
            "without_manifest": sum(1 for b in backups if not b["has_manifest"]),
            "latest": latest["display_name"] if latest else "",
        }

    def _describe_backup(self, folder: Path, files: list[Path]) -> dict[str, Any]:
        rel = folder.relative_to(self.backup_dir)
        name = folder.name
        manifest = folder / "manifest.txt"
        failure = folder / "dashboard_failure.txt"
        total_size = sum(p.stat().st_size for p in files)
        backup_type = self._detect_type(folder)
        expected = self._expected_files(backup_type)
        file_names = {p.name for p in files}
        missing = [f for f in expected if f not in file_names]

        if failure.exists():
            status = "Failed"
            status_message = self._short_failure(failure)
        elif missing:
            status = "Partial"
            status_message = "Backup is missing one or more expected files."
        else:
            status = "Verified"
            status_message = "Expected backup files are present."

        stat = folder.stat()
        created = datetime.fromtimestamp(stat.st_mtime)
        return {
            "name": name,
            "display_name": name.replace("_", " "),
            "path": str(rel),
            "type": backup_type,
            "created": created.strftime("%Y-%m-%d %H:%M"),
            "age": self._age(created),
            "file_count": len(files),
            "total_size": self._format_bytes(total_size),
            "total_size_bytes": total_size,
            "has_manifest": manifest.exists(),
            "status": status,
            "status_message": status_message,
            "missing": missing,
            "files": [{"name": p.name, "size": self._format_bytes(p.stat().st_size)} for p in sorted(files)],
            "manifest": manifest.read_text(encoding="utf-8", errors="replace") if manifest.exists() else "",
            "failure": failure.read_text(encoding="utf-8", errors="replace") if failure.exists() else "",
        }

    def _detect_type(self, folder: Path) -> str:
        name = folder.name.lower()
        rel = str(folder.relative_to(self.backup_dir)).lower()
        if name.startswith("baseline") or "/baseline" in rel or "baseline" in name:
            return "Baseline"
        if name.startswith("runtime") or "/runtime" in rel or "runtime" in rel:
            return "Runtime"
        return "Unknown"

    def _expected_files(self, backup_type: str) -> list[str]:
        if backup_type in ("Runtime", "Baseline"):
            return ["ace_databases.sql.gz", "ace_infrastructure.tar.gz", "manifest.txt"]
        return []

    def _mark_failed_backup(self, backup_name: str | None, exit_code: int, output: str, started: datetime) -> None:
        if not backup_name:
            return
        folder = next((p for p in self.backup_dir.rglob(backup_name) if p.is_dir()), None)
        if folder:
            (folder / "dashboard_failure.txt").write_text(f"Runtime backup failed.\nStarted: {started.isoformat()}\nExit Code: {exit_code}\n\nCaptured Output:\n{output}\n", encoding="utf-8")

    def _extract_backup_name(self, output: str) -> str | None:
        match = re.search(r"/opt/acserver/backups/runtime/([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2})", output)
        if match:
            return match.group(1)
        match = re.search(r"Target\s*:\s*/opt/acserver/backups/runtime/([0-9_\-]+)", output)
        return match.group(1) if match else None

    def _summarize_success(self, output: str, backup_name: str | None) -> str:
        parts = ["Runtime backup completed successfully."]
        if backup_name:
            parts.append(f"Backup: {backup_name}")
        m = re.search(r"Elapsed:\s*([^=]+?)\s+Status", output)
        if m:
            parts.append(f"Duration: {m.group(1).strip()}")
        m = re.search(r"SUCCESS\s+([0-9.]+\s*[A-Za-z]+)", output)
        if m:
            parts.append(f"Size: {m.group(1).strip()}")
        if "Using a password on the command line interface can be insecure" in output:
            parts.append("Warning: mysqldump reported command-line password usage.")
        return " ".join(parts)

    def _summarize_failure(self, exit_code: int, output: str, backup_name: str | None) -> str:
        parts = [f"Runtime backup failed with exit code {exit_code}."]
        if backup_name:
            parts.append(f"Partial backup marked failed: {backup_name}.")
        reason = self._first_error_line(output)
        if reason:
            parts.append(f"Reason: {reason}")
        return " ".join(parts)

    def _first_error_line(self, output: str) -> str:
        for line in output.splitlines():
            lower = line.lower()
            if "error" in lower or "not found" in lower or "cannot" in lower or "failed" in lower:
                return line.strip()[:240]
        return output.strip().splitlines()[-1][:240] if output.strip() else ""

    def _short_failure(self, path: Path) -> str:
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            if line.lower().startswith("exit code"):
                return f"Backup failed. {line}"
        return "Backup failed during dashboard execution."

    def _age(self, dt: datetime) -> str:
        delta = datetime.now() - dt
        minutes = max(0, int(delta.total_seconds() // 60))
        days, rem = divmod(minutes, 1440)
        hours, mins = divmod(rem, 60)
        if days:
            return f"{days}d {hours}h"
        if hours:
            return f"{hours}h {mins}m"
        return f"{mins}m"

    def _format_bytes(self, value: int | float) -> str:
        value = float(value)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024:
                return f"{value:.1f} {unit}"
            value /= 1024
        return f"{value:.1f} PB"
