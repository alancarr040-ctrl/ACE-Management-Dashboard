# ACE Management Dashboard Project Metadata

name: ACE Management Dashboard
version: 2.5.0-dev
phase: 2 - ACE Server Management
milestone: 2.5.0 - Operational Health Dashboard
status: Development
build: 2026.07.08-250

## Current Milestone

2.5.0 adds a read-only Operational Health Dashboard that consolidates ACE service status, disk usage, backup readiness, management wrapper availability, and recent management failures into a compact monitoring page.

## Notes

- Adds `/health` and `/api/health` as read-only operational health views.
- Reuses existing Docker, backup, system, and management service layers.
- Keeps corrective actions on the Management page or SSH/manual workflows.
- Maintains the compact UI principle: new visibility is aggregated into subsystem summaries instead of expanding top-level card count.
