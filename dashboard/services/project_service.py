from __future__ import annotations

import json
import os
import platform
from pathlib import Path
from typing import Dict, Iterable


class ProjectService:
    """Central project metadata provider.

    Project/version information is rendered in the shared Project Information
    card on every page.  Keeping it in one JSON file prevents stale template or
    service defaults from accidentally "de-versioning" the dashboard during
    changed-file package overlays.
    """

    DEFAULTS: Dict[str, str] = {
        "product": "ACE Management Dashboard",
        "version": "unknown",
        "phase": "unknown",
        "milestone": "unknown",
        "status": "Development",
        "build": "unknown",
    }

    def __init__(self, project_file: str | Path | None = None):
        self.project_file = Path(project_file) if project_file else None

    def _candidate_files(self) -> Iterable[Path]:
        if self.project_file:
            yield self.project_file

        env_path = os.environ.get("ACEMD_PROJECT_METADATA")
        if env_path:
            yield Path(env_path)

        # Docker image build context is ./dashboard with WORKDIR /app.
        yield Path("/app/config/project.json")
        yield Path("/app/PROJECT.json")

        # Local/dev fallbacks when running from the repository root.
        here = Path(__file__).resolve()
        dashboard_root = here.parents[1]
        repo_root = here.parents[2] if len(here.parents) > 2 else dashboard_root
        yield dashboard_root / "config" / "project.json"
        yield dashboard_root / "PROJECT.json"
        yield repo_root / "config" / "project.json"

    def _read_json_metadata(self, path: Path) -> Dict[str, str]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return {}
        return {str(key): str(value) for key, value in raw.items() if value is not None}

    def get_info(self) -> Dict[str, str]:
        data = dict(self.DEFAULTS)

        for path in self._candidate_files():
            try:
                if path.exists() and path.is_file():
                    data.update(self._read_json_metadata(path))
                    break
            except (OSError, json.JSONDecodeError, ValueError):
                continue

        data["python"] = platform.python_version()
        return data
