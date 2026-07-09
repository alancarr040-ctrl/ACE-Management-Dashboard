# ACE Management Dashboard

**ACE Management Dashboard** (**ACEMD**) is a web-based management and administration platform for an ACE server stack.

ACEMD is **not** the ACE emulator and is **not** a fork of ACE. ACE refers to the upstream emulator/server project. ACEMD is the companion dashboard, wrapper, monitoring, automation, and administration platform built around an ACE server deployment.

## Current package

| Field | Value |
|---|---|
| Version | 2.9.0-dev |
| Phase | 2 - ACEMD Platform Foundation |
| Milestone | 2.9.0 - Notifications & Alerts |
| Build | 2026.07.09-280 |

## Project direction

The original long-term goal of ACEMD is comprehensive ACE server administration, including accounts, characters, logins/sessions, players, world information, and database tools.

The project intentionally began with the operational platform first:

- Management wrapper.
- Interactive operations console.
- Health dashboard.
- Event journal.
- Automation engine.
- Future metrics and notifications.

These platform services provide the safety, visibility, and auditability needed before building account and character administration modules.

See:

- [`docs/Vision/VISION.md`](docs/Vision/VISION.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`CHANGELOG.md`](CHANGELOG.md)
- [`docs/README.md`](docs/README.md)

## Current capabilities

- Dashboard summary for system disk, Docker, backup, and live ACE status.
- Docker workspace for container inventory, health, logs, and guarded ACE server restart.
- Backup workspace for runtime backup creation, discovery, validation, manifests, and reporting.
- Logs workspace for ACE server, database, and dashboard container logs with filtering.
- Management operations console for whitelisted wrapper actions with output capture, dry-run support, filtering, and collapsible subsystem groups.
- Health workspace for read-only operational status.
- Events workspace for operational monitoring history.
- Automation workspace for request-driven scheduler ticks, registry-backed read-only jobs, Run Now support, relative run times, and job history.
- Metrics workspace for CPU/load, memory, disk, Docker container resources, database container resources, ACEMD internal metrics, and threshold checks.
- About workspace for project metadata.

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

The repository root is intentionally kept small. Long-form documentation lives under `docs/`.

Important project documents:

- `docs/README.md` - documentation index.
- `docs/Vision/VISION.md` - product identity and philosophy.
- `docs/Vision/PROJECT.md` - infrastructure and repository overview.
- `ROADMAP.md` - public project roadmap.
- `CHANGELOG.md` - cumulative release history.
- `docs/AI/AI_ROADMAP.md` - detailed governance roadmap.
- `docs/Architecture/` - architecture and engineering decision records.
- `docs/Automation/` - scheduler and automation documentation.
- `docs/Operations/` - Docker, backups, database, network, recovery, and server operations.
- `docs/Releases/` - per-release package README and release notes.
- `docs/Packages/` - future package definitions.

## Development cleanup

Before packaging or committing:

```bash
scripts/clean-dev.sh
```

This removes `__pycache__`, compiled Python files, and common local cache folders.

The ignored `Test/` directory is reserved for package extraction and deployment testing before accepted changes are copied into the repository for Git review.
