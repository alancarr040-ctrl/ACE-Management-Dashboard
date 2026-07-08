# ACE Management Dashboard

The ACE Management Dashboard is the web management interface for the local ACE Docker server stack.

## Current package

| Field | Value |
|---|---|
| Version | 2.6.0-dev |
| Phase | 2 - ACE Server Management |
| Milestone | 2.6.0 - Operational Monitoring & Events |
| Build | 2026.07.08-241 |

## Current capabilities

- Dashboard summary for system disk, Docker, backup, and live ACE status.
- Docker workspace for container inventory, health, logs, and guarded ACE server restart.
- Backup workspace for runtime backup creation, discovery, validation, manifests, and reporting.
- Logs workspace for ACE server, database, and dashboard container logs with filtering.
- About workspace for project metadata.
- ACE Management Utility wrapper for common stack administration.
- Compact Management operations console for whitelisted wrapper actions with output capture, dry-run support, filtering, and collapsible subsystem groups.

## Deployment

From the project root:

```bash
docker compose up -d --build ace-dashboard
```

Use the dashboard at:

```text
http://<server-ip>:8080/
```

## ACE Management Utility

`manage.sh` is the supported command-line interface for administering the ACE stack.

Common commands:

```bash
./manage.sh status
./manage.sh dashboard rebuild
./manage.sh server logs 150
./manage.sh server restart
./manage.sh db logs 150
./manage.sh backup create
./manage.sh doctor
./manage.sh version
```

2.6.0 adds an Operational Events workspace and event journal for health transitions and management command results. 2.5.0 added the read-only Health page, and 2.4.1 exposes approved wrapper actions through a compact operations console:

```bash
./manage.sh --dry-run restart server
./manage.sh --dry-run server restart
./manage.sh logs server 50
./manage.sh server logs 50
./manage.sh log srv 50
./manage.sh srv log 50
```

Dry-run mode prints the Docker or script command that would run without making changes.

The wrapper is modular and routes subsystem behavior through `scripts/lib/`. Dashboard management actions now use this utility through a whitelisted service layer instead of accepting arbitrary shell commands or embedding one-off Docker Compose commands.

## Development cleanup

Before packaging or committing:

```bash
scripts/clean-dev.sh
```

This removes `__pycache__`, compiled Python files, and common local cache folders.
