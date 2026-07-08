# Changelog

## 2.3.0-dev - 2026-07-08

- Added Phase 2.3 ACE Management Utility wrapper.
- Added `manage.sh` with modular subsystem libraries under `scripts/lib/`.
- Added read-only Management dashboard page documenting wrapper commands.
- Added EDR-0005 - ACE Management Wrapper.
- Updated project metadata to Phase 2.3.

## 2.2.0-dev - 2026-07-08

- Added the Phase 2.2 ACE Log Viewer.
- Added `dashboard/ace/logs.py` for ACE-specific log source handling, severity classification, search filtering, and normalized log entries.
- Updated `/logs` to support source, severity, line count, and search filters.
- Added structured log summary cards and table rendering.
- Added EDR-0004 - ACE Log Viewer.
- Updated project metadata to Phase 2.2.

## 2.1.0-dev - 2026-07-08

- Added live ACE Server Status to the Dashboard.
- Added ACE container, Docker health, database TCP, process, uptime, and recent-error status checks.
- Documented EDR-0003 - Live Server Status.

## 2.3.1-dev - Wrapper Usability Pass

- Added dry-run support to the ACE Management Utility.
- Added command-first and category-first parsing support.
- Added a small set of service and command aliases.
- Updated project metadata and release documentation.


## 2.4.1 - Operations Console Refinement

- Refined the ACE Management Utility page into compact subsystem groups.
- Added action filtering, collapsible sections, command expanders, busy-state buttons, and a shared command output console.
- Adopted the anti-bloat design rule that new actions should live inside existing subsystem groups unless they represent a distinct operational domain.


## 2.4.1a - Docker Compose Provider Hotfix

- Fixed dashboard wrapper execution when Docker Compose plugin is unavailable in the dashboard container.
- Installed docker-compose-plugin in the dashboard image.
- Added provider detection for `docker compose` and `docker-compose`.
- Improved doctor diagnostics for Compose and Docker socket visibility.

## 2.6.1 - Roadmap & Vision

- Added public roadmap, project vision, and product naming standards.
- Established ACE Management Dashboard / ACEMD terminology.
- Clarified the distinction between ACEMD and the ACE emulator/server.
- Documented the path from platform foundation to account, character, player, world, and database administration.
