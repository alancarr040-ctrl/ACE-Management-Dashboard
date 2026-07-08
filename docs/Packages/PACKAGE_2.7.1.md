# PACKAGE 2.7.1 - Repository & Documentation Reorganization

## Purpose

Phase 2.7.1 reorganizes the ACE Management Dashboard documentation tree so the repository root remains clean and GitHub-friendly while preserving all package, release, operations, architecture, and vision documentation under `docs/`.

This is a documentation-structure and governance package. It does not change runtime dashboard behavior.

## Scope

- Keep only repository-level documents in the root.
- Move release-specific README and release notes into `docs/Releases/`.
- Move product vision and infrastructure project documentation into `docs/Vision/`.
- Move engineering decision records into `docs/Architecture/Decisions/`.
- Move operational documents into `docs/Operations/`.
- Move development workflow documents into `docs/Development/`.
- Preserve AI governance under `docs/AI/`.
- Preserve automation documentation under `docs/Automation/`.
- Add documentation index files for the reorganized directories.
- Update root README and governance references to the new structure.

## Root directory standard

The repository root should remain limited to:

- `README.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- `LICENSE`
- `VERSION`
- `.gitignore`
- `.dockerignore`
- Docker Compose files
- Runtime entry points such as `manage.sh`
- Source/runtime directories

Package-specific documentation belongs under `docs/`.

## Deliverables

- Reorganized documentation tree.
- Updated root README documentation links.
- Updated AI engineering standards.
- Updated project metadata for 2.7.1.
- Release notes under `docs/Releases/2.7.1/`.

## Acceptance criteria

- No package README or release note files remain in the repository root.
- Documentation is discoverable through `docs/README.md`.
- Root README points to the new documentation locations.
- Runtime behavior remains unchanged from 2.7.0.
