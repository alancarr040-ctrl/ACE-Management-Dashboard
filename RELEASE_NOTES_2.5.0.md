# Release Notes - 2.5.0 Operational Health Dashboard

## Summary

ACE Management Dashboard 2.5.0 introduces a read-only operational health view for compact monitoring of the ACE stack.

## Added

- Health tab and `/health` route.
- `/api/health` JSON endpoint.
- Health aggregation service using existing Docker, backup, system, and management services.
- Overall health indicator with OK, warning, and critical states.
- Core service health table for dashboard, server, and database containers.
- Disk, backup, wrapper, and recent management failure checks.
- Auto-refresh behavior for the Health page.

## Changed

- Navigation now includes Health.
- Project metadata updated to 2.5.0 development milestone.

## Safety

No new state-changing actions are introduced in this package.

## Known Limitations

- Resource charts are intentionally deferred to a future monitoring phase.
- Dashboard restart/rebuild remains SSH/manual recommended until queued task and reconnect handling are designed.
