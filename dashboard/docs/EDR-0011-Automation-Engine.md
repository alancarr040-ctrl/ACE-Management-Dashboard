# EDR-0011 - ACEMD Automation Engine

## Status

Accepted for 2.7.0 testing.

## Context

ACEMD needs recurring operational awareness without becoming a raw cron manager. Health, Events, backups, and wrapper validation benefit from scheduled read-only checks that publish results into the operational journal.

## Decision

Introduce an ACEMD Automation Engine with built-in jobs and a request-driven scheduler tick. Jobs represent ACEMD operational tasks, not cron entries. Phase 2.7.0 uses runtime JSON state and read-only checks only.

## Consequences

- ACEMD gains an Automation dashboard without requiring a daemon.
- Job history and events become visible immediately.
- Future background workers or plugin-style job registration can replace or extend the scheduler without changing the operator-facing model.
