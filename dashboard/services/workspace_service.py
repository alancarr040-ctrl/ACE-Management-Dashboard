from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkspaceItem:
    key: str
    label: str
    href: str
    description: str
    status: str = "Active"


@dataclass(frozen=True)
class Workspace:
    key: str
    label: str
    href: str
    description: str
    items: tuple[WorkspaceItem, ...]


class WorkspaceService:
    """Shared navigation model for ACEMD workspaces.

    Top-level navigation represents permanent platform workspaces.
    Individual pages are workspace modules and should be grouped here rather
    than added indefinitely to the main navigation bank.
    """

    WORKSPACES: tuple[Workspace, ...] = (
        Workspace(
            "operations",
            "Operations",
            "/operations#operations",
            "Operator actions and controlled changes to the ACEMD environment.",
            (
                WorkspaceItem("management", "Management", "/management#management", "Wrapper-backed ACEMD management actions."),
                WorkspaceItem("docker", "Docker", "/docker#docker", "Container status and supported container actions."),
                WorkspaceItem("backups", "Backups", "/backups#backups", "Runtime backup creation, validation, and inventory."),
                WorkspaceItem("automation", "Automation", "/automation#automation", "Scheduled and rule-driven platform jobs."),
                WorkspaceItem("notifications", "Notifications", "/notifications#notifications", "Operator-facing alerts and notification lifecycle."),
            ),
        ),
        Workspace(
            "monitoring",
            "Monitoring",
            "/monitoring#monitoring",
            "Read-only operational state, telemetry, event history, and logs.",
            (
                WorkspaceItem("health", "Health", "/health#health", "Current operational health and degraded-state checks."),
                WorkspaceItem("metrics", "Metrics", "/metrics#metrics", "Resource and ACEMD internal metrics without dashboard bloat."),
                WorkspaceItem("events", "Events", "/events#events", "Operational event journal and lifecycle history."),
                WorkspaceItem("logs", "Logs", "/logs#logs", "Filtered container log views for operator review."),
            ),
        ),
        Workspace(
            "administration",
            "Administration",
            "/administration#administration",
            "Future Phase 3 ACE administration modules and configuration surfaces.",
            (
                WorkspaceItem("servers", "Servers", "/administration/servers#servers", "ACE connection and profile discovery."),
                WorkspaceItem("accounts", "Accounts", "/administration/accounts#accounts", "Read-only account explorer."),
                WorkspaceItem("characters", "Characters", "/administration/characters#characters", "Read-only character explorer."),
                WorkspaceItem("world", "World", "/administration/world#world", "Read-only world data explorer."),
                WorkspaceItem("relationships", "Relationships", "/administration/relationships#relationships", "Read-only ACE relationship explorer."),
                WorkspaceItem("database", "Database", "/administration/database#database", "Schema and table explorer."),
                WorkspaceItem("configuration", "Configuration", "/administration#administration", "Planned platform configuration module.", "Planned"),
            ),
        ),
        Workspace(
            "tools",
            "Tools",
            "/tools#tools",
            "Utility and diagnostic tools that support ACEMD operations.",
            (
                WorkspaceItem("diagnostics", "Diagnostics", "/tools#tools", "Planned diagnostic workspace utilities.", "Planned"),
                WorkspaceItem("import", "Import", "/tools#tools", "Planned import tooling.", "Planned"),
                WorkspaceItem("export", "Export", "/tools#tools", "Planned export tooling.", "Planned"),
                WorkspaceItem("maintenance", "Maintenance", "/tools#tools", "Planned maintenance utilities.", "Planned"),
                WorkspaceItem("api", "API", "/tools#tools", "Planned API inspection and support utilities.", "Planned"),
                WorkspaceItem("developer", "Developer Tools", "/tools#tools", "Planned developer support workspace.", "Planned"),
            ),
        ),
    )

    MODULE_TO_WORKSPACE = {
        item.key: workspace.key
        for workspace in WORKSPACES
        for item in workspace.items
    }
    MODULE_TO_WORKSPACE.update({"account_detail": "administration", "character_detail": "administration", "character_relationships": "administration"})

    def get_navigation(self, active_tab: str) -> dict:
        active_workspace = self.get_workspace_for_tab(active_tab)
        return {
            "active_workspace": active_workspace,
            "workspaces": [self._workspace_dict(workspace) for workspace in self.WORKSPACES],
            "active_items": self.get_workspace_items(active_workspace),
        }

    def get_workspace(self, key: str) -> dict | None:
        for workspace in self.WORKSPACES:
            if workspace.key == key:
                return self._workspace_dict(workspace)
        return None

    def get_workspace_for_tab(self, active_tab: str) -> str:
        if active_tab in {"dashboard", "about"}:
            return active_tab
        if active_tab in {workspace.key for workspace in self.WORKSPACES}:
            return active_tab
        return self.MODULE_TO_WORKSPACE.get(active_tab, "dashboard")

    def get_workspace_items(self, workspace_key: str) -> list[dict]:
        workspace = self.get_workspace(workspace_key)
        return workspace["items"] if workspace else []

    def _workspace_dict(self, workspace: Workspace) -> dict:
        return {
            "key": workspace.key,
            "label": workspace.label,
            "href": workspace.href,
            "description": workspace.description,
            "items": [item.__dict__ for item in workspace.items],
        }
