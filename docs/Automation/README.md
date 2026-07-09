# ACEMD Automation Engine

The ACEMD Automation Engine is the scheduler and recurring job framework for the ACE Management Dashboard.

Phase 2.7.0 introduced a conservative, read-only automation foundation. Phase 2.7.2 refines that foundation with a registry-backed job model and shared UI time-formatting helpers. It does not edit cron, does not perform destructive maintenance, and does not run restart/rebuild operations. Its purpose is to establish the job model, scheduler state, job history, and event publication path that later automation features will build upon.

## Design Goals

- Keep automation centered on ACEMD jobs rather than raw cron entries.
- Use safe read-only jobs first.
- Publish job results to the ACEMD Events subsystem.
- Maintain compact job history without requiring a database migration.
- Preserve the separation between Health, Events, Management, and Automation.

## Runtime Model

The current Automation Engine uses a request-driven scheduler tick. When the Automation page or `/api/automation` endpoint is read, ACEMD checks whether built-in jobs are due and runs safe jobs as needed.

This avoids adding a daemon or cron dependency before the project has a dedicated background worker. Future versions may add a worker container, cron bridge, or systemd timer while preserving the same job interface.

## Built-in Jobs

The current built-in registry includes:

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

## Job Registry

Phase 2.7.2 introduces an in-process `AutomationJobRegistry`. Built-in jobs are registered as metadata-bearing `AutomationJob` objects with identifiers, schedules, categories, dependencies, and runner callbacks. Future subsystems should register jobs through this registry rather than modifying the scheduler loop.

## Future Work

Future releases may add external plugin discovery, enable/disable persistence, job detail pages, and a dedicated worker container while preserving the same job metadata model.
