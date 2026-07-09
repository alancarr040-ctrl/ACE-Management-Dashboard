# Package 2.7.2 - Automation Framework & UI Polish

## Purpose

Refine the ACEMD Automation Engine introduced in 2.7.0 by establishing a small job registry foundation and improving shared UI presentation patterns.

## Scope

- Introduce automation job metadata and registry objects.
- Move built-in jobs behind the registry.
- Add shared time-formatting utilities.
- Display relative time first with muted absolute timestamps.
- Apply the time display pattern to Automation and Events.
- Update project metadata, documentation, release notes, and roadmap.

## Out of scope

- Host daemon scheduler.
- Cron editor.
- Write-capable or destructive scheduled jobs.
- External plugin loading.
- Metrics and alerts.

## Acceptance checks

- `/automation` loads without error.
- `/api/automation` returns JSON.
- Manual **Run Now** works for read-only jobs.
- Registered jobs show category and dependency metadata.
- Last Run displays values like `just now`, `2 minutes ago`, or `Never`.
- Next Run displays values like `in 15 seconds`, `in 5 minutes`, or `Pending`.
- Muted UTC timestamps remain available below relative values.
- `/events` shows relative event times and muted absolute timestamps.
