# ACEMD Automation Job Architecture

An ACEMD automation job represents an operational task known to the dashboard. Jobs are intentionally higher-level than cron entries.

## Job Fields

Each job has:

- `id` - stable machine-readable identifier.
- `name` - human-readable job name.
- `group` - subsystem or operational domain.
- `schedule` - human-readable schedule label.
- `interval_seconds` - scheduler interval used by the Phase 2.7 request-driven engine.
- `description` - operator-facing purpose.
- `enabled` - whether the job is currently active.
- `runner` - function that performs the read-only check.

## Result Fields

Each run returns:

- `level` - `ok`, `warning`, or `critical`.
- `status` - short result label.
- `detail` - operator-facing details.

## Event Publishing

Each job run records an automation event through the shared Events subsystem. This keeps the Events page as the operational journal for ACEMD.

## Phase 2.7.0 Limitations

The first automation engine intentionally avoids destructive jobs, job editing, cron integration, and plugin discovery. Those are future extensions.
