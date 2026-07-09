# Release Notes - 3.0.1 ACE Data Explorer

3.0.1 builds on the certified 3.0.0 ACE Read-Only Data Foundation by turning the initial read-only Administration modules into practical ACE data explorers.

## Added

- Read-only account detail explorer with linked characters.
- Read-only character detail explorer with representative ACE property sampling.
- Clickable Database Explorer table detail views with columns, indexes, live row counts, and redacted sample rows.
- Table detail links from the database inventory.
- Centralized `dashboard/config/project.json` metadata source loaded by `ProjectService`.

## Improved

- Account detail queries now tolerate optional ACE account columns that may not exist in every ACE schema.
- Database table detail views normalize MySQL/MariaDB `information_schema` key casing before rendering.
- Wide schema/sample-row tables now use horizontal scrolling instead of expanding the page layout.
- Wide Database Explorer tables keep the first identifying column sticky where supported.

## Safety

- All ACE data access remains routed through `ACEDataService`.
- Mutation SQL remains rejected by the ACE Data Service guard.
- Password hashes, salts, and sensitive sample-row fields remain redacted.
- No write actions, edit forms, delete buttons, or mutation routes are included.

## SQL

No SQL migration required.
