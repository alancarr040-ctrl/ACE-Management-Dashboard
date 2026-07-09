# ACE Data Service

ACEMD 3.0.0 introduces the ACE Data Service as the only supported gateway between ACEMD Administration modules and ACE database information.

The service is intentionally read-only in this release.

## Responsibilities

- Discover ACE database connection profiles from environment variables or `/opt/acserver/.env`.
- Connect to ACE auth, shard, and world databases when configured.
- Inspect schemas through `information_schema`.
- Provide safe table inventories and estimated row counts.
- Provide initial read-only account, character, world, and database views.
- Reject SQL statements that are not explicitly read-only.

## Boundary

ACEMD is the management platform. ACE databases are managed game data.

Administration modules should consume `ACEDataService` rather than embedding SQL in routes, templates, or future feature modules.

## Read-only enforcement

3.0.0 allows only read-style SQL prefixes such as `SELECT`, `SHOW`, `DESCRIBE`, and `EXPLAIN`. Mutation keywords such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE`, `GRANT`, and `REVOKE` are blocked by the service layer.

This release exposes no write actions, no edit forms, and no destructive operations.
