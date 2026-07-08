from __future__ import annotations

from ace.logs import ACELogService
from ace.status import ACEStatusService
from services.backup_service import BackupService
from services.docker_service import DockerService
from services.project_service import ProjectService
from services.system_service import SystemService
from services.management_service import ManagementService

docker_service = DockerService()
backup_service = BackupService()
project_service = ProjectService()
system_service = SystemService()
management_service = ManagementService()
ace_status_service = ACEStatusService(docker_service)
ace_log_service = ACELogService(docker_service)


def common_context(active_tab: str, message: dict | None = None):
    containers = docker_service.get_containers()
    backups = backup_service.list_backups()
    latest_backup = backups[0] if backups else None
    return {
        "active_tab": active_tab,
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
        "message": message,
    }
