# ACEMD 3.0.1 Testing Notes

Package: 3.0.1 - ACE Schema Discovery

## Test Areas

1. Rebuild the dashboard container because `requirements.txt` adds PyMySQL.
2. Open Administration > Servers.
3. Confirm ACE database profiles are discovered.
4. Open Administration > Database.
5. Confirm baseline schema inventory is visible even if live DB connection is unavailable.
6. Confirm Accounts, Characters, and World pages render without mutation actions.
7. If live DB credentials are available inside `/opt/acserver/.env`, confirm read-only rows/counts appear.

## Expected Commands

```bash
docker compose up -d --build ace-dashboard
```

## Safety

This package is read-only. It does not include SQL migrations or write actions.
