# ACE Management Dashboard Project Metadata

name: ACE Management Dashboard
version: 2.7.2-dev
phase: 2 - ACEMD Platform Foundation
milestone: 2.7.2 - Automation Framework & UI Polish
status: Development
build: 2026.07.08-272

## Current Milestone

2.7.2 refines the Automation subsystem by introducing a plugin-style in-process job registry, job metadata, shared time formatting helpers, and consistent relative/absolute timestamp presentation across Events and Automation views.

## Notes

- The Automation Engine remains request-driven and read-only.
- Built-in automation jobs are now registered through a shared job registry rather than being embedded directly in the scheduler loop.
- Operator-facing times now show human-readable relative values first, with muted UTC timestamps retained for auditability.
- This phase prepares ACEMD for future subsystem-provided automation jobs.
