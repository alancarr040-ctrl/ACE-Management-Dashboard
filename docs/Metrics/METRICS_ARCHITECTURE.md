# Metrics Architecture

The ACEMD Metrics Service is a shared read-only service that aggregates resource measurements from the dashboard runtime, Docker, storage paths, ACEMD services, and future ACE data collectors.

## Responsibilities

The Metrics Service owns:

- Gathering current resource measurements.
- Normalizing values into UI-ready structures.
- Applying thresholds.
- Producing OK/warning/critical classifications.
- Providing data to `/metrics` and `/api/metrics`.
- Providing metric snapshots to the Automation Engine.

## Current Collectors

| Collector | Source | Notes |
|---|---|---|
| CPU | OS load average | Normalized by CPU count. |
| Memory | `/proc/meminfo` | Uses available memory where possible. |
| Storage | `shutil.disk_usage` | Project and backup filesystem views. |
| Docker | Docker SDK stats | Per-container CPU, memory, network, restart, uptime, and health information. |
| Database | Docker container metrics | SQL-level metrics deferred to ACE data integration. |
| ACEMD | Existing services | Wrapper action count, automation job status, event counts. |

## Relationship to Other Services

Metrics is not a replacement for Health. Metrics explains resource pressure; Health answers whether the platform is operational.

Metrics is not a replacement for Events. Metrics can publish or support events when thresholds change, but Events remains the operational journal.

Metrics is not a replacement for Automation. Automation schedules recurring metric snapshots and future maintenance checks.

Metrics is not a replacement for Notifications. Notifications, planned for Phase 2.9.0, will use Metrics thresholds as one of its inputs.

## Future Integration

Future ACE administration phases may add domain-specific metrics:

- Players online.
- Server tick or loop health.
- Landblock/object counts.
- Database connections and query rates.
- Character/account operation rates.
- Login/session trends.

Those should be registered as collectors instead of being hard-coded into UI pages.
