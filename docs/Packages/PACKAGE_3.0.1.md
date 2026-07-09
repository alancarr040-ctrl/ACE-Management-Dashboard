# Package 3.0.1 - ACE Schema Discovery

## Summary

Introduces the first certifiable Phase 3 ACE Data Foundation work by adding read-only schema discovery and explorer pages to the Administration workspace.

## Scope

- Add ACEDataService.
- Add guarded read-only SQL access.
- Add ACE database profile discovery from environment files.
- Add Administration routes for Servers, Accounts, Characters, World, and Database.
- Add baseline schema documentation from the ACE initialization database dump.
- Add PyMySQL dependency for live MySQL access.

## No SQL Migration

No ACEMD database migration is required.

## Safety

This package exposes no edit, delete, update, or mutation actions.
