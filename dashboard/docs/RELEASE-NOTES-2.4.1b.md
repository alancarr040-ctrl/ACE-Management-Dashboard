# Release Notes - 2.4.1b Operations Console Safety Hotfix

## Summary

Phase 2.4.1b applies a minimal safety refinement after live testing showed that dashboard rebuild/restart actions interrupt the browser session because the command restarts the container serving the web UI.

## Changes

- Keeps session-interrupting full-stack and dashboard lifecycle commands visible for documentation.
- Disables normal web Run buttons for dashboard rebuild/restart and full-stack lifecycle actions.
- Leaves Dry Run available for those actions so command validation can still be tested from the browser.
- Adds operator-facing manual/SSH guidance beside disabled actions.
- Adds backend enforcement so disabled web actions cannot be executed by POSTing directly to the route.

## Deferred

Queued host-side command execution and browser reconnect/refresh behavior are deferred to a future operations-runner phase.
