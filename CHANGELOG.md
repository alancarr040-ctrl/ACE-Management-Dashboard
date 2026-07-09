# Changelog

## 3.1.1 - ACE Knowledge Base Foundation

### Added

- Added read-only ACE Knowledge Base module under Administration.
- Added initial property dictionary seed entries for observed character string properties.
- Added confidence/provenance model for raw ACE property interpretation.
- Added controlled observation plan for discovering property meanings through before/after tests.
- Added route `/administration/knowledge`.
- Added Administration workspace navigation entry for Knowledge.

### Fixed

- Fixed Account Management summary card access for the `clear` count so Jinja does not resolve Python's dictionary `clear` method.

### Changed

- Updated project metadata to 3.1.1-dev.
- Updated package documentation for the new semantic translation layer.

### Notes

- No write operations were added.
- No SQL migration is required.
