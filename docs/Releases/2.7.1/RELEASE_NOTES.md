# Release Notes - 2.7.1 Repository & Documentation Reorganization

## Overview

Phase 2.7.1 standardizes the ACE Management Dashboard repository documentation layout.

## Added

- `docs/README.md` documentation index.
- `docs/Architecture/README.md`.
- `docs/Development/README.md`.
- `docs/Operations/README.md`.
- `docs/Releases/README.md`.
- `docs/Vision/README.md`.
- `docs/Packages/PACKAGE_2.7.1.md`.

## Changed

- Moved release-specific package READMEs from the repository root to `docs/Releases/<version>/README.md`.
- Moved release-specific notes from the repository root to `docs/Releases/<version>/RELEASE_NOTES.md`.
- Moved `PROJECT.md` and `VISION.md` to `docs/Vision/`.
- Moved engineering decision records to `docs/Architecture/Decisions/`.
- Moved operational documentation to `docs/Operations/`.
- Moved development workflow documentation to `docs/Development/`.
- Updated root `README.md` to reference the new documentation structure.
- Updated metadata to `2.7.1-dev`.

## Removed

- Removed the accidental `docs/test.txt` artifact.

## Runtime impact

No runtime behavior changes are intended. This package is documentation-only aside from project metadata updates.
