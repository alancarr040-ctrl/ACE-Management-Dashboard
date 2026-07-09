# ACE Management Dashboard Project Metadata

name: ACE Management Dashboard
version: 3.0.0-dev
phase: 3 - ACE Administration Foundation
milestone: 3.0.0 - Read-Only ACE Data Foundation
status: Development
build: 2026.07.09-300

## Current Milestone

3.0.0 begins Phase 3 by introducing ACEMD's ACE Data Service and the first read-only Administration modules for ACE-facing data.

## Notes

- ACEMD owns the management platform boundary.
- ACE data access is routed through ACEDataService.
- Phase 3.0.0 is read-only by design.
- Administration now includes Servers, Accounts, Characters, World, and Database read-only discovery pages.
- Future write or management features must build on this service foundation rather than bypassing it.
