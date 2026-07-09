# ACE Management Dashboard

ACEMD is a management platform that sits above ACE.

Current milestone: **3.0.1 — ACE Data Explorer**

Phase 3 establishes safe ACE-facing administration foundations. ACE data access is routed through ACEDataService and remains read-only until explicit future administration phases introduce controlled write workflows.

Project metadata is sourced from `dashboard/config/project.json` and rendered through `ProjectService` to prevent stale template defaults from de-versioning the dashboard.
