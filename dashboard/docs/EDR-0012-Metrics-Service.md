# EDR-0012 - Metrics Service

## Decision

ACEMD will provide a dedicated Metrics Service and Metrics workspace beginning in Phase 2.8.0.

## Rationale

Metrics are a cross-cutting platform concern. Resource data such as CPU load, memory use, disk capacity, container stats, wrapper status, automation status, and event volume will be useful to Health, Automation, Notifications, and future ACE administration modules.

Implementing metrics as a shared service avoids embedding one-off resource collection logic in individual pages.

## Scope

Phase 2.8.0 provides current-state, read-only operational metrics:

- CPU/load summary.
- Memory summary.
- Project and backup disk usage.
- Docker container resource metrics.
- Database container resource summary.
- ACEMD internal metrics.
- Threshold checks.
- `/metrics` and `/api/metrics`.
- Metrics Snapshot automation job.

## Non-goals

- Full telemetry database.
- Graph-heavy dashboards.
- External alert delivery.
- SQL-level database profiling.
- ACE runtime/game metrics.

## Consequences

Future ACEMD modules should consume Metrics Service data instead of collecting their own resource metrics. If a metric may be reused by more than one subsystem, it should be promoted to the Metrics Service.
