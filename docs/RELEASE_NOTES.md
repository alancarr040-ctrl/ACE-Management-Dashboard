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

---

# ACE Management Dashboard 2.4.1 - Operations Console Refinement

## Summary

Phase 2.4.1 refines the Phase 2.4.0 wrapper integration into a more compact operations console without expanding the number of primary cards.

## Changes

- Reworked the Management page into subsystem-level collapsible groups.
- Added compact wrapper status tiles for readiness, mode, version, and action count.
- Added a shared command output console for the most recent action result.
- Added client-side action filtering to reduce scrolling.
- Moved shell command visibility behind per-action "Show command" expanders.
- Added guarded submit behavior with confirmation prompts and busy button labels.
- Preserved whitelisted wrapper execution, dry-run support, and audit history from 2.4.0.

## Design Principle

New management capability should be integrated into existing subsystem groups whenever practical. New cards should be introduced only for distinct subsystems or operational domains.

## Testing Notes

Deploy over the existing 2.4.0 package and rebuild/restart the dashboard container. Validate the Management page, run a read-only command, run a dry-run change action, and confirm that recent activity updates.
