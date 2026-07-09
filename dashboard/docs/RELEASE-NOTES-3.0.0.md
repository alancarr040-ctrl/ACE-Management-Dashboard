# ACEMD 3.0.0 - Read-Only ACE Data Foundation

3.0.0 begins Phase 3 by introducing the ACE Data Service and the first read-only ACE-facing Administration modules.

## Added

- `ACEDataService` for centralized ACE database access.
- Read-only SQL enforcement in the ACE data layer.
- Administration routes for:
  - Servers
  - Accounts
  - Characters
  - World
  - Database
- Schema discovery and table inventory through `information_schema`.
- Safe account and character discovery with search and row limits.
- World table-of-interest discovery.
- `/api/administration/ace-data` read-only API endpoint.
- PyMySQL dependency for ACE database connectivity.
- ACE Data Service documentation.

## Safety

This package intentionally does not include write actions, edit forms, destructive operations, account changes, character changes, or world changes.

## SQL migration

No SQL migration is required.
