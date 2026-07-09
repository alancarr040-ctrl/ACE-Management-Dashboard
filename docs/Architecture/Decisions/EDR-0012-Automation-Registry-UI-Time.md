# EDR-0012 - Automation Registry and Relative Time UI

## Status

Accepted for Phase 2.7.2 testing.

## Context

Phase 2.7.0 introduced the ACEMD Automation Engine with built-in read-only jobs. Testing showed that the operator experience would be clearer if future scheduled times were displayed as relative countdowns such as `in 15 minutes` while still retaining absolute timestamps for auditability. The scheduler also needed to move away from hard-coded job lists before future subsystems begin contributing jobs.

## Decision

Introduce a small in-process automation job registry and shared UI time-formatting helpers.

The registry defines jobs as metadata-bearing objects with:

- Identifier
- Name
- Group/category
- Schedule
- Interval
- Description
- Dependencies
- Runner callback
- Event publication behavior

Operator-facing time displays should show relative time first and muted absolute UTC timestamps second.

## Consequences

- Built-in jobs no longer require direct scheduler-loop edits.
- Future subsystem job registration has a defined path.
- Automation and Events use a consistent time display pattern.
- The scheduler remains request-driven and read-only until a future worker/daemon phase is explicitly designed.
