# ACE Management Dashboard Project Metadata

name: ACE Management Dashboard
version: 3.0.1a-dev
phase: 3 - ACE Data Foundation
milestone: 3.0.1a - ACE Schema Discovery Polish
status: Development
build: 2026.07.09-301a

## Current Milestone

3.0.1a polishes ACE schema discovery display and live character/account verification fields for the Administration workspace.

## Notes

- ACE-facing Administration modules route database access through ACEDataService.
- Mutation SQL is rejected by the read-only query guard.
- Schema baseline is documented from the ACE initialization database dump.
- Accounts, Characters, World, and Database pages are read-only explorers, not management editors.
