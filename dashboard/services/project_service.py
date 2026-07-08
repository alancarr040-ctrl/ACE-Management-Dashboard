from __future__ import annotations

from pathlib import Path
from typing import Dict
import platform


class ProjectService:
    def __init__(self, project_file: str | Path = "/app/PROJECT.md"):
        self.project_file = Path(project_file)

    def get_info(self) -> Dict[str, str]:
        data = {
            "product": "ACE Management Dashboard",
            "version": "2.2.0-dev",
            "phase": "2 - ACE Server Management",
            "milestone": "2.2 - ACE Log Viewer",
            "status": "Development",
            "build": "2026.07.08-220",
            "python": platform.python_version(),
        }

        if self.project_file.exists():
            for line in self.project_file.read_text(encoding="utf-8").splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                if key.strip() and value.strip():
                    data[key.strip()] = value.strip()

        return data
