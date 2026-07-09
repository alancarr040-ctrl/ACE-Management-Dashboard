# ACE Discovery Framework

Phase 3.0 establishes ACEMD's read-only discovery framework for ACE data.

The discovery framework exists to understand ACE before ACEMD performs any write-capable administration.

## Principles

1. Discover before modifying.
2. Read-only before read-write.
3. Schema-aware, never schema-assumed where practical.
4. Pages use services, not direct database access.
5. Sensitive fields are redacted before template rendering.
6. Mutation SQL is blocked by the ACE Data Service guard.

## Phase 3.0 packages

| Package | Purpose |
|---|---|
| 3.0.0 | ACE read-only data foundation. |
| 3.0.1 | ACE schema and table explorer. |
| 3.0.2 | ACE relationship explorer. |
| 3.0.3 | Foundation polish and stabilization. |

## Service boundary

All ACE database access belongs in:

```text
dashboard/services/ace_data_service.py
```

Templates and routes must not issue SQL directly.

## Read-only guard

The ACE Data Service accepts only read-only SQL prefixes such as `SELECT`, `SHOW`, `DESCRIBE`, `DESC`, and `EXPLAIN`. Mutation keywords such as `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `DROP`, and `TRUNCATE` are rejected.

## Future work

The 3.1 through 3.5 administration modules should build on this discovery framework. Write-capable actions must remain out of the ACE Data Service until a dedicated write-safety framework is designed, audited, and certified.
