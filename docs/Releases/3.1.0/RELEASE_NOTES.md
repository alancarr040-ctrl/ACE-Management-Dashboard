# Release Notes - 3.1.0 Account Management

## Added

- Initial read-only Account Management subsystem.
- Account summary metrics for total accounts, clear accounts, banned accounts, and accounts with linked characters.
- Account search by name or id.
- Status, access-level, sort, pagination, and per-page controls.
- Administrator-oriented account result table that hides sensitive credential fields.
- Schema-aware optional account columns for ACE database compatibility.

## Changed

- Project metadata advanced from 3.0.3 Discovery Foundation Polish to 3.1.0 Account Management.
- Account list now presents administrative summaries rather than raw discovery output.

## Safety

- Read-only enforcement remains in `ACEDataService`.
- No SQL migration is included.
- No write endpoints or mutation controls are introduced.
