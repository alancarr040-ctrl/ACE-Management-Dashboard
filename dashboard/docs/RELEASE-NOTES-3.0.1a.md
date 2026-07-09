# Release Notes - 3.0.1a ACE Schema Discovery Polish

## Summary

3.0.1a is a focused polish/testing package for the Phase 3 read-only ACE Data Foundation.

It corrects Database Explorer table rendering and improves live account/character verification fields without adding any mutation actions.

## Changes

- Fixed schema table-name rendering when MySQL/MariaDB returns information_schema keys as uppercase.
- Added read-only account character counts.
- Added read-only linked account names to character results.
- Normalized ACE BIT fields before display.
- Continued enforcing ACE Data Service read-only SQL guard.

## Safety

No SQL migrations are included. No write actions are exposed.
