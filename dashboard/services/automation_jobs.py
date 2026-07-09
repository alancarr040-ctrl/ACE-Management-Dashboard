from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

JobRunner = Callable[[], dict[str, Any]]


@dataclass(frozen=True)
class AutomationJob:
    id: str
    name: str
    group: str
    schedule: str
    interval_seconds: int
    description: str
    runner: JobRunner
    enabled: bool = True
    category: str = "Core"
    owner: str = "ACEMD"
    version: str = "1.0"
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    produces_events: bool = True

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "group": self.group,
            "schedule": self.schedule,
            "interval_seconds": self.interval_seconds,
            "description": self.description,
            "enabled": self.enabled,
            "category": self.category,
            "owner": self.owner,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "produces_events": self.produces_events,
        }


class AutomationJobRegistry:
    """Small plugin-style registry for ACEMD automation jobs.

    Phase 2.7.2 keeps discovery explicit and in-process, but moves the scheduler away
    from a hard-coded list.  Future packages can register jobs from subsystem modules
    without changing the scheduler loop.
    """

    def __init__(self) -> None:
        self._jobs: dict[str, AutomationJob] = {}

    def register(self, job: AutomationJob) -> None:
        if job.id in self._jobs:
            raise ValueError(f"Automation job already registered: {job.id}")
        self._jobs[job.id] = job

    def get(self, job_id: str) -> AutomationJob | None:
        return self._jobs.get(job_id)

    def all(self) -> list[AutomationJob]:
        return sorted(self._jobs.values(), key=lambda job: (job.group, job.name))

    def groups(self) -> dict[str, list[AutomationJob]]:
        grouped: dict[str, list[AutomationJob]] = {}
        for job in self.all():
            grouped.setdefault(job.group, []).append(job)
        return grouped

    def __iter__(self) -> Iterable[AutomationJob]:
        return iter(self.all())
