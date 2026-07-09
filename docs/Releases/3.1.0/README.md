# ACE Management Dashboard 3.1.0 Testing Notes

Package 3.1.0 begins the Account Management administration subsystem.

The account module remains read-only. It consumes ACE data through `ACEDataService` and does not expose password hashes, salts, mutation buttons, or write endpoints.

## Test focus

- Open `/administration/accounts`.
- Confirm the page presents Account Management rather than raw table discovery.
- Test search by account name and account id.
- Test status filter: all, clear, banned.
- Test access-level filtering when access levels are present.
- Test sorting by name, id, access, characters, last login, total logins, and created date.
- Test pagination and per-page selection.
- Open an account detail page and confirm linked characters still display.
- Confirm character links route back into the existing read-only character detail page.

## Safety expectations

- No SQL migration is required.
- No account mutation actions are present.
- Password, salt, hash, token, and secret fields are redacted or excluded.
