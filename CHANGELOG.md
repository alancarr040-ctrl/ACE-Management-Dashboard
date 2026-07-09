# Changelog

## 3.0.1a - ACE Schema Discovery Polish

- Fixed live schema inventory table-name rendering across MySQL/MariaDB information_schema key casing.
- Added account character counts to the read-only Account Explorer.
- Added linked account names to the read-only Character Explorer when available.
- Normalized ACE BIT fields before template rendering so deleted/plussed flags display correctly.
- Preserved read-only ACE Data Service enforcement and mutation guard.

## 3.0.1 - ACE Schema Discovery

- Added ACEDataService as the read-only gateway for ACE database access.
- Added Administration explorer routes for Servers, Accounts, Characters, World, and Database.
- Added ACE schema baseline for auth, shard, and world databases based on the initialization dump.
- Added guarded SQL read-only enforcement for ACE data queries.
- Added PyMySQL dependency for live ACE MySQL inspection.
- Added ACE schema discovery and read-only pattern documentation.

## 2.9.1 - Workspace & Navigation Framework

- Added Workspace Service as the shared navigation model.
- Reorganized main navigation into Dashboard, Operations, Monitoring, Administration, Tools, and About.
- Added workspace landing pages for Operations, Monitoring, Administration, and Tools.
- Added secondary navigation for modules within each workspace.
- Preserved existing page URLs for all Phase 2 modules.
- Added navigation framework documentation.

## 2.9.0 - Notifications & Alerts

- Added shared Notification Service.
- Added Notifications workspace, API, and navigation alert badge.
- Added local/dashboard notification delivery.
- Added alert lifecycle actions for acknowledge and resolve.
- Added Health, Metrics, Automation, and critical Event alert rules.
- Added notification channel registry for future outbound delivery providers.
- Added notification architecture and release documentation.

# ACE Management Dashboard Changelog

This changelog summarizes certified project milestones. Detailed release notes remain available in the per-package release documentation under `docs/Releases/`.

## 2.8.0 - Metrics & Resource Monitoring

- Added ACEMD Metrics Service.
- Added Metrics workspace and `/api/metrics`.
- Added CPU/load, memory, project disk, and backup disk metrics.
- Added Docker container CPU, memory, network, restart, health, and uptime metrics.
- Added database container resource summary.
- Added ACEMD internal metrics for wrapper, automation, and events.
- Added resource threshold checks.
- Added Metrics Snapshot automation job.
- Added Metrics documentation and EDR-0012.

## 2.7.2 - Automation Framework & UI Polish

- Added automation job metadata objects and a registry foundation.
- Moved built-in automation jobs behind the registry.
- Added shared relative/future time formatting helpers.
- Added shared severity badge helper.
- Updated Automation to show relative Last Run and Next Run values with muted UTC timestamps.
- Updated Events to show relative time first with muted UTC timestamps.
- Updated project metadata to 2.7.2.

## 2.7.1 - Repository & Documentation Reorganization

Documentation-structure release.

- Reorganized release-specific README and release notes into `docs/Releases/`.
- Moved product vision and project overview documentation into `docs/Vision/`.
- Moved engineering decision records into `docs/Architecture/Decisions/`.
- Moved operational documentation into `docs/Operations/`.
- Moved development workflow documentation into `docs/Development/`.
- Added documentation index files for the reorganized `docs/` tree.
- Removed accidental `docs/test.txt` artifact.
- Updated project metadata to 2.7.1.

## 2.7.0 - Scheduler & Automation

- Added ACEMD Automation Engine foundation.
- Added Automation dashboard tab and `/automation` route.
- Added `/api/automation` endpoint.
- Added request-driven scheduler tick.
- Added built-in read-only jobs for Health, backups, disk usage, wrapper validation, and event journal validation.
- Added manual **Run Now** support for safe jobs.
- Added automation job history.
- Added automation event publishing.
- Added `docs/Automation/` documentation.
- Updated `.gitignore` to ignore `Test/`.

## 2.6.1 - Roadmap & Vision

Documentation-only release.

- Added top-level `ROADMAP.md` for GitHub-facing project direction.
- Added top-level `VISION.md` defining the ACEMD product identity and philosophy.
- Established **ACE Management Dashboard** as the official product name.
- Established **ACEMD** as the approved short name.
- Clarified that ACEMD is not ACE and is not an ACE fork.
- Documented why the project began with operations before account and character administration.
- Added public roadmap sections for platform foundation, ACE server administration, and advanced platform work.
- Updated governance and package documentation for Phase 2.7.0.

## 2.6.0 - Operational Monitoring & Events

- Added Events workspace.
- Added event API.
- Added health transition tracking.
- Added management command event logging.
- Established the event journal as a shared operational history layer.

## 2.5.0 - Operational Health Dashboard

- Added Health workspace.
- Added health API.
- Added compact service status, disk, backup, wrapper, and recent failure checks.
- Established the Health page as the read-only operational state view.

## 2.4.x - Interactive Management

- Added compact Management operations console.
- Added wrapper-backed action execution.
- Added dry-run support and whitelisted actions.
- Added safety restrictions for disruptive web-triggered restart and rebuild actions.

## 2.3.x - Management Wrapper Foundation

- Established `manage.sh` as the supported ACEMD management wrapper.
- Added documentation and governance standards for future wrapper-backed operations.
