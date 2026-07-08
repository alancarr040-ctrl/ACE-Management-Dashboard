# EDR-0004 - ACE Log Viewer

## Status

Accepted

## Context

Phase 2 moves the dashboard from infrastructure-only operations into ACE Server Management. Phase 2.1 established live server status. The next operational need is a usable log workspace for troubleshooting ACE runtime behavior without requiring SSH access for every check.

## Decision

The Logs workspace will use an ACE-specific log service instead of embedding Docker log access directly in the route or template.

The service provides:

- Known ACE-related log sources.
- Safe line limits.
- Basic severity classification.
- Search filtering.
- Normalized entries for template rendering.
- Summary counts for operational triage.

## Rationale

Logs are an ACE operations feature, not just a Docker feature. Keeping log parsing in `dashboard/ace/logs.py` preserves the existing architecture and leaves room for later file-based ACE log parsing, database-backed events, and richer diagnostics.

## Current scope

- Container log sources only.
- Read-only log viewing.
- No destructive actions.
- No persistent audit trail yet.

## Future work

- Add ACE file log sources from `/opt/acserver/ace/Logs`.
- Add time-window filtering.
- Add export/download support.
- Add deeper ACE-specific parsing when log formats are fully documented.
