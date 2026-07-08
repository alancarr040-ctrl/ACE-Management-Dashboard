# PACKAGE 2.7.0 - Scheduler & Automation

## Package status

Implemented for testing.

## Product name

This package is for **ACE Management Dashboard** (**ACEMD**), the management platform for ACE server deployments. It is not a package for the ACE emulator itself.

## Objective

Implement the first ACEMD Scheduler & Automation framework.

The goal is not to automate every maintenance task immediately. The goal is to establish a reusable background job foundation that future ACEMD subsystems can use safely.

## Scope

Phase 2.7.0 introduces:

- Automation/Scheduler workspace.
- Built-in read-only job definitions.
- Job status API.
- Job history storage.
- Manual run support for safe jobs.
- Enabled/disabled display for built-in jobs.
- Event publication for job completions and failures.
- Initial read-only or low-risk jobs such as health polling, backup freshness check, disk threshold check, and wrapper availability check.

## Out of scope

- Full alerting/notification delivery.
- Metrics dashboards.
- Account or character administration.
- Long-running dashboard rebuild orchestration.
- Autonomous destructive remediation.

## Design constraints

- Keep the UI compact.
- Do not create one card per tiny task.
- Represent jobs in tables or compact groups.
- Publish scheduler activity to Events.
- Do not duplicate Health or Management functionality.
- Preserve ACEMD naming standards.

## Deliverables

- Updated source.
- Scheduler/Automation page and API.
- Initial job definitions.
- Event integration.
- README package documentation.
- Release notes.
- Documentation updates.
- Deployment ZIP.
