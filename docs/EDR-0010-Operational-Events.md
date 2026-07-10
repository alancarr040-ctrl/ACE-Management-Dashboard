# EDR-0010 - Operational Events

## Status

Accepted for Phase 2.6.0 development package.

## Context

Phase 2.5.0 introduced a read-only Health page that reports the current state of the ACE stack. Testing confirmed that the dashboard can detect transitions from Healthy to Critical to Warning and back to Healthy, but the interface did not retain a concise timeline of those transitions.

## Decision

Introduce a lightweight operational event layer that records important state changes and management command outcomes without adding a database dependency or a background worker. Events are persisted as JSONL under the existing runtime backup area. The current health snapshot is stored separately and compared on each Health/API observation to generate transition events only when state changes.

## Scope

Phase 2.6.0 records:

- Overall health state changes.
- Core service state or health changes.
- Initial health observation.
- Management command completion or failure.

## Non-Goals

- No alert delivery.
- No email, SMS, webhook, or external notification integration.
- No database schema migration.
- No queued task runner.
- No automatic remediation.

## Rationale

The JSONL event journal is sufficient for the current single-host ACE deployment model and preserves the no-bloat design direction. It gives operators a compact timeline while avoiding the complexity of a full monitoring stack.

## Consequences

The Health page remains the current-state view. The Events page becomes the change-over-time view. Future monitoring, alerting, or notification features can consume the same event model without changing the Health page architecture.
