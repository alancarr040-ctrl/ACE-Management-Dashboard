# EDR-0005 - ACE Management Wrapper

## Status
Accepted for Phase 2.3 development testing.

## Context
The ACE Management Dashboard now includes Docker management, backups, live server status, and a structured log viewer. Administrative actions were beginning to depend directly on Docker Compose command details. That creates duplicated implementation paths between SSH operations, documentation, dashboard services, and future automation.

## Decision
Introduce `manage.sh` as the canonical ACE Management Utility for stack administration.

The wrapper provides a stable operator interface for:

- System status, start, stop, restart, and rebuild
- Dashboard logs, shell, restart, and rebuild
- ACE server status, logs, shell, and restart
- Database status, logs, shell, and restart
- Backup create, list, and verify
- Doctor/health checks
- Version and help output

The wrapper is intentionally modular. `manage.sh` is the command router, while subsystem functions live under `scripts/lib/`.

## Safety Boundary
Phase 2.3 exposes wrapper documentation in the dashboard as a read-only Management page. The dashboard does not execute wrapper actions in this milestone. Runtime execution from the web interface is deferred until command authorization, audit logging, and confirmation workflows are designed.

## Consequences
Future dashboard services should call the wrapper instead of directly embedding Docker Compose commands whenever administrative action execution is required. Documentation should prefer `./manage.sh ...` examples as the supported operator interface.
