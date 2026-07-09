# ACEMD 3.0.1a Testing Notes

Package: 3.0.1a - ACE Schema Discovery Polish

## Test Areas

1. Rebuild the dashboard container.
2. Open Administration > Servers and confirm all three ACE databases connect.
3. Open Administration > Database and confirm table names render instead of `None`.
4. Open Administration > Accounts and confirm the Characters column appears.
5. Create one live ACE character, then open Administration > Characters and confirm the character appears.
6. Confirm no edit, delete, save, mutation, or administrative write actions are exposed.

## Expected Command

```bash
docker compose up -d --build ace-dashboard
```

## Safety

This package remains read-only. It does not include SQL migrations or write actions.
