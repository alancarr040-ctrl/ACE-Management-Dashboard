# Release Notes - 2.2.0-dev

## Milestone

Phase 2.2 - ACE Log Viewer

## Summary

This package continues Phase 2 ACE Server Management by replacing the placeholder logs page with a structured operations log viewer.

## Added

- ACE log integration service at `dashboard/ace/logs.py`.
- Multi-source log selection for ACE Server, ACE Database, and ACE Dashboard containers.
- Log severity classification for error, warning, and info entries.
- Search filtering across timestamp and message text.
- Line limit selector for 50, 100, 150, 250, and 500 lines.
- Log summary cards showing raw counts and filtered result counts.
- Table-based log display with timestamp, severity, and message columns.
- Engineering decision record EDR-0004.

## Changed

- Project metadata advanced from 2.1 to 2.2.
- Legacy marker files now match Phase 2 project metadata.
- Logs route now uses the ACE log service rather than directly dumping server logs.
- Dashboard CSS extended for filter controls and structured tables.

## Preserved

- Existing service, route, manager, and ACE subsystem architecture.
- Docker CLI installation inside the dashboard container.
- Backup creation, validation, and reporting behavior.
- Live server status behavior from Phase 2.1.
- MySQL networking fix status; this package does not change MySQL networking.

## Deployment

```bash
docker compose up -d --build ace-dashboard
```
