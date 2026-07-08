# EDR-0001 - ACE Management Dashboard Architecture

## Status

Accepted and evolving.

## Context

The ACE Management Dashboard is intended to become the long-term administrative console for the ACE Docker server. It began as a status page but is now being developed as a modular management application.

## Decision

The dashboard will follow these architectural rules:

1. The dashboard presentation layer does not own business logic.
2. Routes and tabs stay thin.
3. Business logic belongs in reusable managers.
4. Existing administrative scripts remain reusable from SSH, cron, automation, and the dashboard.
5. Python APIs are preferred over shell commands where practical.
6. The Dashboard tab is a summary view.
7. Dedicated tabs are subsystem workspaces.
8. Project metadata is provided by `ProjectManager` and rendered consistently across the application.

## Current Managers

- `ProjectManager`
  - Product name
  - Version
  - Phase
  - Milestone
  - Status
  - Build
  - Runtime information

- `DockerManager`
  - Container inventory
  - Container health
  - Container details
  - Recent logs
  - Summary counts

- `BackupManager`
  - Backup set discovery
  - Manifest detection
  - Backup validation
  - Backup metadata

- `SystemManager`
  - Disk usage
  - Future server health integration

## UI Model

The application uses tabs as subsystem workspaces:

- Dashboard: operational summary
- Docker: Docker management workspace
- Backups: backup management workspace
- Logs: log viewing workspace
- About: project and runtime information

Future tabs may include:

- Restore
- Accounts
- Characters
- World
- Configuration
- Maintenance

## Development Workflow

Production-style deployment bakes the dashboard source into the Docker image and requires a rebuild after code/template changes.

Development mode should use bind mounts and Flask auto-reload where practical to reduce iteration time.

## Documentation Policy

Documentation should support engineering, not replace it. For this project, documentation should remain lightweight and useful:

- README
- Release Notes / Changelog
- Roadmap
- EDR-0001

Additional EDRs should be added only for major architectural decisions.

## v0.6 Update - First Docker Management Action

The first enabled Docker action is container restart. This action follows the established architecture:

1. The template renders a POST form.
2. The route remains thin.
3. The route calls `DockerManager.restart_container()`.
4. The manager performs the Docker SDK operation and returns a normalized result dictionary.
5. The route reports the result through a flash message and redirects back to the Docker workspace.

Start, Stop, Remove, and Recreate remain disabled until confirmation flows, authentication/authorization, and audit logging are available.
