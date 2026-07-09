# ACE Management Dashboard 2.7.2

## Automation Framework & UI Polish

This release refines the 2.7 Automation Engine by moving built-in jobs behind a small registry interface and improving operator-facing timestamps throughout Automation and Events.

2.7.2 is intentionally conservative: the scheduler remains request-driven, jobs remain read-only, and no host daemon or cron editor is introduced.

## Test focus

- Confirm `/automation` loads.
- Confirm registered jobs appear with relative Last Run and Next Run values.
- Confirm muted UTC timestamps remain visible below relative times.
- Run a safe job manually with **Run Now**.
- Confirm `/events` shows relative event times with muted UTC timestamps.
- Confirm `/api/automation` and `/api/events` still return JSON.
