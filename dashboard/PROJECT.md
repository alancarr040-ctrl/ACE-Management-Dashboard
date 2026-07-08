# ACE Management Dashboard Project Metadata

name: ACE Management Dashboard
version: 2.6.0-dev
phase: 2 - ACE Server Management
milestone: 2.6.0 - Operational Monitoring & Events
status: Development
build: 2026.07.08-250

## Current Milestone

2.6.0 adds an Operational Events layer that records health transitions and management command results in a compact JSONL event journal. The Health page remains read-only while now surfacing recent events, and the new Events workspace provides a filtered event timeline.

## Notes

- Adds `/health` and `/api/health` as read-only operational health views.
- Reuses existing Docker, backup, system, and management service layers.
- Keeps corrective actions on the Management page or SSH/manual workflows.
- Maintains the compact UI principle: new visibility is aggregated into subsystem summaries instead of expanding top-level card count.
