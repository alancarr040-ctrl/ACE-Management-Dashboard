# Release Notes - 2.3.0-dev

## Phase 2.3 - Management Wrapper

This development package introduces the ACE Management Utility wrapper.

## Added

- `manage.sh` command-line management utility.
- Modular wrapper libraries under `scripts/lib/`.
- Commands for system, dashboard, server, database, backup, maintenance, version, and help workflows.
- Read-only dashboard Management page documenting available wrapper commands.
- `dashboard/services/management_service.py` and `dashboard/routes/management_routes.py`.
- EDR-0005 - ACE Management Wrapper.

## Changed

- Project metadata updated to 2.3.0-dev.
- Navigation now includes Management.
- Documentation now prefers the wrapper as the operator-facing management interface.

## Notes

The dashboard Management page is read-only in this milestone. It does not execute wrapper commands from the web interface.
