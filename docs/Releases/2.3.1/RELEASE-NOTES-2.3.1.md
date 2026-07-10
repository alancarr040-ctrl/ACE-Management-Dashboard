# Release Notes - ACE Management Dashboard 2.3.1-dev

## Milestone

Phase 2.3.1 - Wrapper Usability Pass

## Summary

This development release improves the ACE Management Utility introduced in 2.3.0.

## Changes

- Added `--dry-run` / `-n` support for commands that would change stack state.
- Added command-first forms such as `restart server`, `logs server 50`, and `shell db`.
- Preserved category-first forms such as `server restart`, `server logs 50`, and `db shell`.
- Added limited aliases:
  - `dash` for dashboard
  - `srv` and `ace` for server
  - `database` and `mysql` for db
  - `log` for logs
  - `reboot` for restart
- Updated wrapper help text and metadata.

## Testing Focus

Test both command orders and dry-run behavior:

```bash
./manage.sh --dry-run restart server
./manage.sh --dry-run server restart
./manage.sh --dry-run rebuild dashboard
./manage.sh logs server 50
./manage.sh server logs 50
./manage.sh log srv 50
./manage.sh srv log 50
```

Dry-run commands should print the command that would be executed without changing container state.
