# ACE Management Dashboard 2.6.0 - Operational Monitoring & Events

This package builds on the accepted 2.5.0 Operational Health Dashboard release.

## Purpose

Phase 2.6.0 introduces a lightweight operational event layer so ACE can show not only the current health state, but also what changed over time. The implementation remains intentionally compact and does not add destructive controls or a database dependency.

## Included Changes

- Adds `EventService` with a local JSONL event journal.
- Adds `/events` navigation tab and filtered event timeline.
- Adds `/api/events` JSON endpoint.
- Records health transitions such as Healthy → Warning → Critical → Healthy.
- Records management command results as operational events.
- Adds recent operational events to the Health page without expanding the core dashboard layout.
- Renames recent management failure wording to recent command errors for clarity.
- Updates dashboard metadata and engineering documentation for 2.6.0.

## Event Storage

Events are stored by default in:

```bash
/opt/acserver/backups/runtime/operational-events.jsonl
```

The last observed health snapshot is stored by default in:

```bash
/opt/acserver/backups/runtime/health-state.json
```

Both paths can be overridden with environment variables if needed:

- `ACE_EVENTS_LOG`
- `ACE_EVENTS_STATE`
- `ACE_EVENTS_MAX`

## Deployment

Extract the package over the accepted ACE Management Dashboard tree, then rebuild the dashboard container:

```bash
docker compose up -d --build ace-dashboard
```

## Testing Checklist

1. Confirm Dashboard, Docker, Backups, Logs, Management, Health, Events, and About tabs load.
2. Open `/health` and confirm recent operational events are displayed or an empty-state message appears.
3. Open `/events` and confirm the event timeline renders.
4. Open `/api/events` and confirm JSON is returned.
5. Stop `ace-server` with `docker compose stop ace-server`, wait for Health to turn Critical, then start it again.
6. Confirm Events records the service and overall health transitions.
7. Run a safe Management action such as Version or Help and confirm the command result appears in Events.

## Safety Notes

The event layer is observational. It records state transitions and command results but does not execute corrective actions. Corrective actions remain on the Management page or SSH/manual workflows.
