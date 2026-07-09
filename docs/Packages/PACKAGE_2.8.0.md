# Package 2.8.0 - Metrics & Resource Monitoring

## Objective

Introduce the ACEMD Metrics Service and compact resource monitoring workspace so operators can understand resource pressure without leaving the dashboard.

## Implemented Scope

- Metrics Service for shared read-only resource collection.
- `/metrics` UI workspace.
- `/api/metrics` JSON endpoint.
- CPU/load summary normalized by CPU count.
- Memory summary from `/proc/meminfo`.
- Project and backup filesystem usage.
- Docker container CPU, memory, network, restart, health, and uptime metrics.
- Database container resource summary.
- ACEMD internal metrics for wrapper, automation, and events.
- Threshold checks for CPU, memory, disk, container, and database state.
- Metrics Snapshot automation job.
- Metrics documentation and architecture notes.

## Constraints Preserved

- Metrics remain read-only.
- No external notifications were added; notifications remain Phase 2.9.0.
- No graph-heavy UI or telemetry database was introduced.
- SQL-level database metrics and ACE runtime/game metrics are deferred to later phases.

## Test Checklist

- Rebuild `ace-dashboard`.
- Open `/metrics` and confirm the Metrics workspace renders.
- Open `/api/metrics` and confirm JSON returns.
- Verify CPU, memory, disk, container, database, and ACEMD metric sections display.
- Confirm existing Health, Events, Automation, Management, Docker, Backups, Logs, and About pages still render.
- Open Automation and confirm Metrics Snapshot is registered.
- Run Metrics Snapshot manually and confirm an automation event appears.

## Documentation Updated

- `ROADMAP.md`
- `CHANGELOG.md`
- `README.md`
- `docs/Metrics/README.md`
- `docs/Metrics/METRICS_ARCHITECTURE.md`
- `docs/Packages/PACKAGE_2.8.0.md`
- `docs/Packages/PACKAGE_2.9.0.md`
- `dashboard/docs/EDR-0012-Metrics-Service.md`
- `dashboard/docs/RELEASE-NOTES-2.8.0.md`
