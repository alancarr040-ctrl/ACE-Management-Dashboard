# Release Notes - 3.0.3 Foundation Polish

ACEMD 3.0.3 is a stabilization package for the Phase 3.0 ACE Discovery Framework.

## Highlights

- Centralized project metadata through `dashboard/config/project.json`.
- Hardened `ProjectService` so version, milestone, status, and build metadata are loaded from one source of truth.
- Added compatibility fallback to legacy flat metadata files.
- Updated wide table behavior in discovery views.
- Added documentation for the Project Metadata Service and ACE Discovery Framework.

## Safety

This package does not add ACE write actions and does not require a SQL migration.
