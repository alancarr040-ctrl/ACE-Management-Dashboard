# ACE Management Dashboard Changelog

This changelog summarizes certified project milestones. Detailed release notes remain available in the per-package release documentation.

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
