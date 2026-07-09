# Release Notes - 2.7.2

## Summary

Phase 2.7.2 adds the first ACEMD Automation Framework refinements and shared UI time-formatting polish.

## Added

- `dashboard/services/automation_jobs.py`
  - `AutomationJob` metadata object.
  - `AutomationJobRegistry` for plugin-style job registration.
- `dashboard/utils/time_format.py`
  - Shared relative time formatter.
  - Shared future countdown formatter.
  - Shared muted absolute UTC timestamp formatter.
- `dashboard/utils/status.py`
  - Shared severity-to-badge mapping helpers.

## Changed

- Automation jobs are now registered through the job registry instead of a hard-coded scheduler list.
- Automation job rows now show metadata including category and dependencies.
- Automation Last Run and Next Run values now show human-readable relative time first.
- Muted UTC timestamps remain visible under relative time values for auditability.
- Event timeline entries now show relative time first with absolute UTC time underneath.
- Automation event panels now use the same time display style.
- Project metadata updated to 2.7.2.

## Safety

- No destructive automation actions were added.
- No cron/systemd timers were created.
- No database migrations are required.
- Existing 2.7.0 request-driven scheduler behavior is preserved.

## Known limitations

- Job discovery is still explicit and in-process.
- Enable/disable persistence remains future work.
- Subsystem-provided plugin jobs are prepared for but not yet broadly integrated.
