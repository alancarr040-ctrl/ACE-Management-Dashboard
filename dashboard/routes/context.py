from __future__ import annotations

from ace.logs import ACELogService
from ace.status import ACEStatusService
from services.backup_service import BackupService
from services.docker_service import DockerService
from services.project_service import ProjectService
from services.system_service import SystemService
from services.management_service import ManagementService
from services.health_service import HealthService
from services.event_service import EventService
from services.automation_service import AutomationService
from services.automation_jobs import AutomationJob
from services.metrics_service import MetricsService
from services.notification_service import NotificationService
from services.workspace_service import WorkspaceService

docker_service = DockerService()
backup_service = BackupService()
project_service = ProjectService()
system_service = SystemService()
management_service = ManagementService()
health_service = HealthService(docker_service, backup_service, system_service, management_service)
event_service = EventService()
automation_service = AutomationService(health_service, backup_service, system_service, management_service, event_service)
metrics_service = MetricsService(docker_service, system_service, backup_service, management_service, event_service)
metrics_service.bind_automation(automation_service)
notification_service = NotificationService(health_service, metrics_service, automation_service, event_service)
workspace_service = WorkspaceService()


def _run_metrics_snapshot():
    metrics = metrics_service.get_metrics()
    overall = metrics.get("overall", {})
    summary = metrics.get("summary", {})
    return {
        "level": overall.get("level", "unknown"),
        "status": overall.get("label", "Unknown"),
        "detail": f"CPU {summary.get('cpu', 'Unknown')}, memory {summary.get('memory', 'Unknown')}, disk {summary.get('disk', 'Unknown')}."
    }


automation_service.registry.register(AutomationJob(
    "metrics_snapshot",
    "Metrics Snapshot",
    "Metrics",
    "Every minute",
    60,
    "Collects the read-only ACEMD metrics snapshot and applies resource thresholds.",
    _run_metrics_snapshot,
    category="Metrics",
    dependencies=("metrics_service", "event_service"),
))
ace_status_service = ACEStatusService(docker_service)
ace_log_service = ACELogService(docker_service)


def common_context(active_tab: str, message: dict | None = None):
    containers = docker_service.get_containers()
    backups = backup_service.list_backups()
    latest_backup = backups[0] if backups else None
    return {
        "active_tab": active_tab,
        "workspace_nav": workspace_service.get_navigation(active_tab),
        "project": project_service.get_info(),
        "containers": containers,
        "docker_summary": docker_service.get_summary(),
        "docker_resources": docker_service.get_resources(),
        "backups": backups,
        "backup_summary": backup_service.get_summary(),
        "backup_storage": backup_service.get_storage_summary(),
        "latest_backup": latest_backup,
        "disk": system_service.get_disk_usage(),
        "ace_status": ace_status_service.get_status(),
        "log_sources": ace_log_service.get_sources(),
        "notification_summary": notification_service.get_center(refresh=False)["summary"],
        "message": message,
    }
