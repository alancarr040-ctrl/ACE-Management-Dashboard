from __future__ import annotations

import json
import os
import platform
from pathlib import Path
from typing import Dict, Iterable


class ProjectService:
    """Central project metadata provider.

    ACEMD renders project identity, version, phase, milestone, status, and
    build information in the shared header and About page.  Those values must
    come from one metadata source so changed-file package overlays cannot
    accidentally reintroduce stale template or service defaults.

    Primary source:
        dashboard/config/project.json

    Compatibility fallbacks:
        dashboard/VERSION, dashboard/PHASE, dashboard/MILESTONE,
        dashboard/STATUS, dashboard/BUILD
    """

    DEFAULTS: Dict[str, str] = {
        "product": "ACE Management Dashboard",
        "short_name": "ACEMD",
        "version": "unknown",
        "phase": "unknown",
        "milestone": "unknown",
        "status": "Development",
        "build": "unknown",
        "metadata_source": "defaults",
    }

    LEGACY_FILES = {
        "version": "VERSION",
        "phase": "PHASE",
        "milestone": "MILESTONE",
        "status": "STATUS",
        "build": "BUILD",
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

    def _dashboard_root(self) -> Path:
        return Path(__file__).resolve().parents[1]

    def _read_json_metadata(self, path: Path) -> Dict[str, str]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return {}
        data = {str(key): str(value) for key, value in raw.items() if value is not None}
        data["metadata_source"] = str(path)
        return data

    def _read_legacy_metadata(self) -> Dict[str, str]:
        """Read legacy flat metadata files only when JSON metadata is absent.

        These files are retained because older packages already used them, but
        the JSON metadata file is the certified source of truth for Phase 3.0.3
        and later.
        """
        root = self._dashboard_root()
        data: Dict[str, str] = {}
        for key, filename in self.LEGACY_FILES.items():
            path = root / filename
            try:
                if path.exists() and path.is_file():
                    value = path.read_text(encoding="utf-8").strip()
                    if value:
                        data[key] = value
            except OSError:
                continue
        if data:
            data["metadata_source"] = str(root)
        return data

    def get_info(self) -> Dict[str, str]:
        data = dict(self.DEFAULTS)

        loaded = False
        for path in self._candidate_files():
            try:
                if path.exists() and path.is_file():
                    data.update(self._read_json_metadata(path))
                    loaded = True
                    break
            except (OSError, json.JSONDecodeError, ValueError):
                continue

        if not loaded:
            data.update(self._read_legacy_metadata())

        data["python"] = platform.python_version()
        return data
