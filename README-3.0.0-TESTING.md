# ACEMD 3.0.0 Testing Package

This package contains changed files only for ACEMD 3.0.0 - Read-Only ACE Data Foundation.

## Install

Apply the files over a certified 2.9.1 ACEMD repository, then rebuild the dashboard container:

```bash
docker compose up -d --build ace-dashboard
```

## Test focus

- Administration workspace loads.
- Servers opens `/administration/servers`.
- Accounts opens `/administration/accounts`.
- Characters opens `/administration/characters`.
- World opens `/administration/world`.
- Database opens `/administration/database`.
- Existing Operations, Monitoring, Tools, and About pages still load.
- No edit/write/destructive actions are displayed on the new Administration pages.

## Dependency note

3.0.0 adds `PyMySQL==1.1.1` to `dashboard/requirements.txt` so the dashboard can connect to the ACE MySQL databases.

## SQL migration

No SQL migration is required.
