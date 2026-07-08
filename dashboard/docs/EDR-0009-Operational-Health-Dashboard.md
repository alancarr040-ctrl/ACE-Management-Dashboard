# EDR-0009 - Operational Health Dashboard

## Status

Accepted for Phase 2.5.0 development.

## Context

After wrapper integration, the dashboard needs operational visibility without increasing the number of management action cards or adding risky controls.

## Decision

Add a read-only Health workspace backed by a dedicated health aggregation service. The service consumes existing Docker, backup, system, and management service layers and converts their results into normalized OK, warning, and critical checks.

## Consequences

- Health visibility improves without expanding the Management action surface.
- Individual subsystem failures are displayed as health findings rather than unhandled route failures.
- Corrective actions remain on Management or SSH/manual workflows.
- Future monitoring features can extend the health service without changing the UI navigation model.
