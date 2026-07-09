# Release Notes - 2.8.0 Metrics & Resource Monitoring

Phase 2.8.0 introduces the ACEMD Metrics Service and Metrics workspace.

## Added

- Metrics navigation tab.
- `/metrics` UI workspace.
- `/api/metrics` JSON endpoint.
- Shared `MetricsService` collector.
- CPU/load, memory, project disk, and backup disk summaries.
- Docker container CPU, memory, network, restart, health, and uptime metrics.
- Database container resource summary.
- ACEMD internal metrics for wrapper actions, automation jobs, and event counts.
- Threshold checks for CPU, memory, disk, containers, and database container state.
- Metrics Snapshot automation job.
- Metrics documentation under `docs/Metrics/`.
- EDR-0012 documenting the Metrics Service decision.

## Notes

Metrics are read-only and intentionally compact. Phase 2.8.0 does not attempt to replace a dedicated telemetry stack or add external alerts. Notifications are planned for Phase 2.9.0.
