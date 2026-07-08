# ACEMD Automation Engine

The ACEMD Automation Engine is the scheduler and recurring job framework for the ACE Management Dashboard.

Phase 2.7.0 introduces a conservative, read-only automation foundation. It does not edit cron, does not perform destructive maintenance, and does not run restart/rebuild operations. Its purpose is to establish the job model, scheduler state, job history, and event publication path that later automation features will build upon.

## Design Goals

- Keep automation centered on ACEMD jobs rather than raw cron entries.
- Use safe read-only jobs first.
- Publish job results to the ACEMD Events subsystem.
- Maintain compact job history without requiring a database migration.
- Preserve the separation between Health, Events, Management, and Automation.

## Runtime Model

Phase 2.7.0 uses a request-driven scheduler tick. When the Automation page or `/api/automation` endpoint is read, ACEMD checks whether built-in jobs are due and runs safe jobs as needed.

This avoids adding a daemon or cron dependency before the project has a dedicated background worker. Future versions may add a worker container, cron bridge, or systemd timer while preserving the same job interface.

## Built-in Jobs

Phase 2.7.0 includes:

- Health Monitor
- Backup Verification
- Disk Usage Check
- Wrapper Validation
- Event Journal Check

All included jobs are read-only.

## Runtime Files

Automation state is stored under the runtime directory, normally:

```text
/opt/acserver/backups/runtime/automation-state.json
```

The path can be overridden with `ACEMD_AUTOMATION_STATE`.

## Future Work

Phase 2.7.1 is expected to introduce plugin-style job registration so subsystems can register jobs without editing the scheduler core.
