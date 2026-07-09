# ACE Management Dashboard Project Metadata

name: ACE Management Dashboard
version: 2.8.0-dev
phase: 2 - ACEMD Platform Foundation
milestone: 2.8.0 - Metrics & Resource Monitoring
status: Development
build: 2026.07.09-280

## Current Milestone

2.8.0 introduces the ACEMD Metrics Service, Metrics workspace, metrics API, resource threshold checks, container resource views, and the Metrics Snapshot automation job.

## Notes

- Metrics are read-only and compact by design.
- ACEMD does not attempt to replace a full telemetry stack in this phase.
- Metrics become a shared platform service for Health, Automation, Notifications, and future ACE administration modules.
- SQL-level and ACE runtime/game metrics are deferred to later data integration phases.
