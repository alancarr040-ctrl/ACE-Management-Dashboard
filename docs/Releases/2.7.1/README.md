# ACE Management Dashboard 2.7.1 Package README

## Package

**2.7.1 - Repository & Documentation Reorganization**

## Type

Documentation and repository-structure update.

## Summary

This package reorganizes documentation so the project root remains clean and focused on repository identity. Release notes, package READMEs, product vision, project overview, operational documentation, development standards, and engineering decision records now live under logical `docs/` subdirectories.

No runtime dashboard behavior is changed by this package.

## Test notes

After applying this package:

1. Confirm the dashboard still starts normally.
2. Confirm GitHub Desktop shows documentation moves rather than unexpected runtime code changes.
3. Confirm the repository root contains only high-level repository files and source/runtime directories.
4. Confirm `docs/README.md` provides the new documentation index.
