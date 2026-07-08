# PACKAGE 2.5.0 - Operational Health Dashboard

## Statement of Work

Implement a compact, read-only operational health dashboard for ACE Management Dashboard.

## Objectives

- Provide a single Health page summarizing the operational state of the ACE stack.
- Reuse existing Docker, backup, system, and management service layers.
- Avoid adding new action cards or destructive controls.
- Preserve the 2.4.1b operations safety model.
- Fail gracefully when a subsystem cannot be queried.

## Deliverables

- `/health` page.
- `/api/health` endpoint.
- Health aggregation service.
- Navigation and styling updates.
- README and release notes.
- Updated project metadata.

## Acceptance Criteria

- Existing tabs continue to load.
- Health page loads without HTTP 500.
- Health API returns JSON.
- Required service rows appear for ace-dashboard, ace-server, and ace-db.
- No rebuild/restart actions are introduced on the Health page.
