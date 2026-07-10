# ACE Management Dashboard 2.5.0 - Operational Health Dashboard

## Summary
Phase 2.5.0 adds a compact read-only Operational Health Dashboard. This release focuses on visibility, not additional control actions.

## Added
- New Health navigation tab.
- New `/health` page.
- New `/api/health` JSON endpoint.
- Health aggregation service for core containers, disk, backups, wrapper readiness, and recent management failures.
- Lightweight container CPU and memory reporting when Docker statistics are available.
- Auto-refreshing health view with manual refresh control.
- Health-oriented status badges and compact subsystem layout.

## Changed
- Dashboard version advanced to 2.5.0.
- Navigation now separates Health visibility from Management actions.
- Documentation updated with EDR-0009.

## Safety
This release is read-only. It does not re-enable web execution for dashboard rebuild or full-stack restart actions.

## Testing Notes
After deployment, rebuild the dashboard container and visit `/health`. Verify that Dashboard, ACE Server, Database, Disk, Backups, Wrapper, and Recent Management Failures render without requiring any management action to be executed.
