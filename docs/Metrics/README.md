# ACEMD Metrics

Phase 2.8.0 introduces the ACEMD Metrics Service and Metrics workspace.

Metrics are intentionally compact and operational. ACEMD is not trying to replace a full telemetry stack such as Prometheus or Grafana. The Metrics subsystem provides enough resource visibility for operators and future ACEMD services to understand whether the dashboard, ACE server, database, storage, and automation layers are under load.

## Scope

The initial Metrics subsystem provides:

- CPU load summary.
- Memory usage summary.
- Project and backup filesystem usage.
- Docker container CPU, memory, network, restart, health, and uptime indicators.
- Database container resource summary.
- ACEMD internal metrics such as wrapper actions, automation jobs, and event counts.
- Threshold checks that classify metrics as OK, warning, or critical.
- `/metrics` UI workspace.
- `/api/metrics` JSON endpoint.
- A registry-backed automation job named **Metrics Snapshot**.

## Design Principles

- Metrics must be read-only.
- Metrics should explain operational state without creating UI bloat.
- Summary cards should answer the most important questions first.
- Detailed rows should remain compact and scannable.
- Metrics should be available as a shared service for Health, Automation, Notifications, and future ACE administration modules.

## Thresholds

Initial resource thresholds are intentionally simple:

| Metric | Warning | Critical |
|---|---:|---:|
| CPU load | 70% | 90% |
| Memory usage | 75% | 90% |
| Disk usage | 80% | 90% |

These thresholds are service-level defaults and should become configurable in a future package once Notifications and operator preferences exist.

## Limitations

Phase 2.8.0 focuses on current-state operational metrics. It does not yet provide:

- Long-term metric history.
- Graph-heavy dashboards.
- Alert delivery channels.
- SQL-level database performance metrics.
- ACE world/runtime metrics such as players online, tick rate, landblocks, or object counts.

Those capabilities are intentionally reserved for later phases so the Metrics service can stabilize before deep ACE data integration begins.
