from __future__ import annotations

from pathlib import Path
import shutil


class SystemService:
    def __init__(self, project_root: str | Path = "/opt/acserver"):
        self.project_root = Path(project_root)

    def get_disk_usage(self) -> dict[str, str]:
        usage = shutil.disk_usage(self.project_root)
        return {
            "total": self._format_bytes(usage.total),
            "used": self._format_bytes(usage.used),
            "free": self._format_bytes(usage.free),
            "percent": f"{round((usage.used / usage.total) * 100, 1)}%",
        }

    def _format_bytes(self, value: int | float) -> str:
        value = float(value)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024:
                return f"{value:.1f} {unit}"
            value /= 1024
        return f"{value:.1f} PB"
