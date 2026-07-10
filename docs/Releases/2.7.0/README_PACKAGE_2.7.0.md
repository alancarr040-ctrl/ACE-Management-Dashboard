# ACE Management Dashboard 2.7.0 Test Package

## Phase

**2.7.0 - Scheduler & Automation**

## Summary

This package adds the first ACEMD Automation Engine implementation.

The release introduces a new **Automation** tab, `/automation`, `/api/automation`, a request-driven scheduler, built-in read-only jobs, automation run history, and automation event publishing.

## Included Jobs

- Health Monitor
- Backup Verification
- Disk Usage Check
- Wrapper Validation
- Event Journal Check

## Testing Notes

1. Deploy the package.
2. Rebuild/restart the dashboard container.
3. Open `/automation`.
4. Confirm the Automation tab loads.
5. Confirm jobs appear and have schedules.
6. Press **Run Now** on each job.
7. Confirm run history updates.
8. Confirm automation events appear on `/events?source=automation`.
9. Confirm Health, Events, and Management still load.

## Safety

All 2.7.0 automation jobs are read-only. No restart, rebuild, delete, restore, or destructive maintenance jobs are included.
