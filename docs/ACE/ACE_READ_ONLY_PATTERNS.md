# ACE Read-Only Patterns

## Rule

All ACE database reads must go through `ACEDataService`.

Templates and routes must not issue direct SQL.

## Guarded Queries

`ACEDataService` permits only read-only SQL prefixes such as:

- `SELECT`
- `SHOW`
- `DESCRIBE`
- `DESC`
- `EXPLAIN`

Mutation keywords are rejected by the service guard.

## No Secrets in UI

The Administration workspace may show database names, hosts, and configured users. It must not display database passwords, account password hashes, or account salts.

## Foundation First

3.0.1 provides discovery and explorer views only. Future write actions require a separate design package, explicit permission model, event logging, notification hooks, and rollback strategy.
