# ACE Management Dashboard 2.6.0 - Operational Monitoring & Events

## Summary

Phase 2.6.0 adds a lightweight operational event layer to capture health transitions and management command outcomes. This allows ACE to answer the next operational question after current health: what changed?

## Added

- `EventService` for compact JSONL event persistence.
- `/events` tab for operational event review.
- `/api/events` endpoint for event data.
- Health transition detection and event recording.
- Management command result event recording.
- Recent operational events panel on the Health page.

## Changed

- Health wording now distinguishes command errors from operational health failures.
- Dashboard metadata updated to 2.6.0.

## Safety

No new destructive controls were added. Events are read-only and intended for operational awareness.
