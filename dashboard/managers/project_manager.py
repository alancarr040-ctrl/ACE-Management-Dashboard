from __future__ import annotations

from pathlib import Path
from typing import Dict
import platform


class ProjectManager:
    def __init__(self, project_file: str | Path = "/app/PROJECT.md"):
        self.project_file = Path(project_file)

    def get_project_info(self) -> Dict[str, str]:
        data = {
            "product": "ACE Management Dashboard",
            "version": "1.0.0-dev",
            "phase": "1 - Infrastructure Foundation",
            "milestone": "1.0 - Backup Workflow Completion",
            "status": "Development",
            "build": "2026.07.08-100",
            "python": platform.python_version(),
        }

        if self.project_file.exists():
            for line in self.project_file.read_text(encoding="utf-8").splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key and value:
                    data[key] = value

        return data
