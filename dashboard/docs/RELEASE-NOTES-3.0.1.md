# Release Notes - 3.0.1 ACE Schema Discovery

## Added

- ACEDataService read-only data gateway.
- Read-only Administration routes for Servers, Accounts, Characters, World, and Database.
- ACE schema baseline for `ace_auth`, `ace_shard`, and `ace_world`.
- Guarded SQL query layer that rejects mutation-oriented SQL.
- PyMySQL dependency for live ACE MySQL access.
- ACE schema and read-only pattern documentation.

## Changed

- Administration workspace modules now link to real read-only explorer pages.

## SQL

No SQL migration required.
