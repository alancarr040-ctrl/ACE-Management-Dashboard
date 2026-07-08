# ACE Management Dashboard

**ACE Management Dashboard** (**ACEMD**) is a web-based management and administration platform for an ACE server stack.

ACEMD is **not** the ACE emulator and is **not** a fork of ACE. ACE refers to the underlying emulator/server project. ACEMD is the companion dashboard, wrapper, monitoring, automation, and administration platform built around an ACE server deployment.

## Current package

| Field | Value |
|---|---|
| Version | 2.6.1-dev |
| Phase | 2 - ACEMD Platform Foundation |
| Milestone | 2.6.1 - Roadmap & Vision |
| Build | 2026.07.08-261 |

## Project direction

The original long-term goal of ACEMD is comprehensive ACE server administration, including accounts, characters, logins/sessions, players, world information, and database tools.

The project intentionally began with the operational platform first:

- Management wrapper.
- Interactive operations console.
- Health dashboard.
- Event journal.
- Upcoming scheduler, metrics, and notifications.

These platform services provide the safety, visibility, and auditability needed before building account and character administration modules.

See:

- [`VISION.md`](VISION.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`CHANGELOG.md`](CHANGELOG.md)

## Current capabilities

- Dashboard summary for system disk, Docker, backup, and live ACE status.
- Docker workspace for container inventory, health, logs, and guarded ACE server restart.
- Backup workspace for runtime backup creation, discovery, validation, manifests, and reporting.
- Logs workspace for ACE server, database, and dashboard container logs with filtering.
- About workspace for project metadata.
- ACE Management Utility wrapper for common stack administration.
- Compact Management operations console for whitelisted wrapper actions with output capture, dry-run support, filtering, and collapsible subsystem groups.
- Health workspace for read-only operational status.
- Events workspace for operational monitoring history.

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

`manage.sh` is the supported command-line interface for administering the ACE stack through ACEMD-approved workflows.

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

Dry-run mode prints the Docker or script command that would run without making changes:

```bash
./manage.sh --dry-run server restart
./manage.sh --dry-run backup create
```

## Documentation

Important project documents:

- `VISION.md` - product identity and philosophy.
- `ROADMAP.md` - public project roadmap.
- `CHANGELOG.md` - cumulative release history.
- `PROJECT.md` - infrastructure and repository overview.
- `docs/AI/AI_ROADMAP.md` - detailed governance roadmap.
- `docs/Packages/` - future package definitions.

## Development cleanup

Before packaging or committing:

```bash
scripts/clean-dev.sh
```

This removes `__pycache__`, compiled Python files, and common local cache folders.
