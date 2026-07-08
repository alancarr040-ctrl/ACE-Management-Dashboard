# EDR-0006 - Wrapper Usability Pass

## Status

Accepted for 2.3.1-dev

## Context

The ACE Management Utility is intended to be the supported administrative interface for the ACE Docker stack. Administrators may naturally type either category-first commands, such as `server restart`, or command-first commands, such as `restart server`.

The wrapper should reduce cognitive load without becoming an uncontrolled alias engine.

## Decision

The wrapper supports both category-first and command-first forms when intent is unambiguous.

Examples:

```bash
./manage.sh server restart
./manage.sh restart server
./manage.sh server logs 50
./manage.sh logs server 50
./manage.sh db shell
./manage.sh shell db
```

A small alias set is supported:

- `dash` -> `dashboard`
- `srv`, `ace` -> `server`
- `database`, `mysql` -> `db`
- `log` -> `logs`
- `reboot` -> `restart`

The wrapper also supports `--dry-run` and `-n` for change-oriented commands. Dry-run mode prints the underlying command that would execute without making changes.

## Consequences

- Administrators can use the command order that feels natural.
- Documentation can still use one canonical style.
- The alias set remains intentionally small and maintainable.
- Dry-run enables safe validation before running stack-changing actions.
