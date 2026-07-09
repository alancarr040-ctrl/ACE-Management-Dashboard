# Package 3.0.3 - Foundation Polish

## Status

Testing

## Purpose

Stabilize the Phase 3.0 ACE Discovery Framework before moving into 3.1 Account Management.

## Scope

- Centralize project metadata in `dashboard/config/project.json`.
- Harden `ProjectService` with JSON-first metadata loading and legacy fallback support.
- Update version/build flat files for compatibility.
- Improve wide data table handling in discovery views.
- Document the metadata service and ACE Discovery Framework.
- Update README, ROADMAP, CHANGELOG, and release notes.

## Out of scope

- No SQL migration.
- No ACE database writes.
- No account or character mutation actions.
- No new administration feature surface beyond foundation polish.

## Testing notes

After deploying changed files, rebuild the dashboard container and verify:

1. Project Information shows 3.0.3-dev.
2. About page shows the same metadata and metadata source.
3. Administration database table detail pages still scroll horizontally for wide tables.
4. Accounts, Characters, World, Database, and Relationships remain read-only and render correctly.
