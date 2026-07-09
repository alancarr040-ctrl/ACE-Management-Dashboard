# ACEMD AI Roadmap

## Naming standard

The product is **ACE Management Dashboard**. The approved short name is **ACEMD**.

Use **ACE** only for the underlying emulator/server project. Do not use ACE as shorthand for this dashboard project in documentation, roadmap entries, release notes, or future package specifications.

## Roadmap purpose

This document is the governance-oriented roadmap for future AI-assisted development. The public GitHub-facing roadmap is `ROADMAP.md`.

Future packages must update this document when architecture, phase order, subsystem scope, documentation layout, or governance expectations change.

## Current status

| Phase | Name | Status |
|---|---|---:|
| 2.3.x | Management Wrapper | Complete |
| 2.4.x | Interactive Management | Complete |
| 2.5.x | Operational Health | Complete |
| 2.6.0 | Operational Monitoring & Events | Complete |
| 2.6.1 | Roadmap & Vision | Complete |
| 2.7.0 | Scheduler & Automation | Complete |
| 2.7.1 | Repository & Documentation Reorganization | Complete |
| 2.7.2 | Automation Framework & UI Polish | Complete |
| 2.8.0 | Metrics & Resource Monitoring | Complete |
| 2.9.0 | Notifications & Alerts | Complete |
| 2.9.1 | Workspace & Navigation Framework | Current Development |
| 3.0.0 | ACE Data Integration Foundation | Planned |
| 3.1.0 | Account Management | Planned |
| 3.2.0 | Character Management | Planned |
| 3.3.0 | Online Player Management | Planned |
| 3.4.0 | World Administration | Planned |
| 3.5.0 | Database Administration | Planned |

## Development tracks

### Platform foundation track: 2.x

The 2.x track builds the operational foundation for ACEMD.

- Wrapper-backed management.
- Web operations console.
- Health monitoring.
- Event history.
- Scheduler and automation.
- Shared UI helpers.
- Metrics.
- Notifications.
- Workspace navigation framework.

### ACE administration track: 3.x

The 3.x track returns to the original game administration goals.

- ACE data integration.
- Account management.
- Character management.
- Online player/session views.
- World administration.
- Database administration.

### Advanced platform track: 4.x

The 4.x track is reserved for advanced features after the platform and administration tracks are stable.

- AI operations assistant.
- Plugin framework.
- Multi-server management.
- Cluster support.
- Advanced automation.

## Design rules for future AI work

- Preserve product naming: ACEMD is the dashboard; ACE is the emulator/server.
- Prefer compact UI additions over card/page proliferation.
- Health remains read-only.
- Management actions flow through certified wrapper/service layers.
- Events are a shared service, not only a page.
- Automation jobs should publish events.
- Automation jobs should register through the shared registry instead of being hard-coded in the scheduler loop.
- Operator-facing timestamps should use relative time first with muted absolute timestamps retained for auditability.
- Future account and character tools must use shared health, event, and safety services instead of duplicating platform logic.
- Documentation must be updated whenever the roadmap or architecture changes.


## Phase 2.8.0 - Metrics & Resource Monitoring

Phase 2.8.0 introduces the shared ACEMD Metrics Service, Metrics workspace, metrics API, threshold checks, Docker/container resource metrics, system resource metrics, database container metrics, and the Metrics Snapshot automation job. Metrics remain read-only and compact. Full alert delivery is reserved for Phase 2.9.0.


## Phase 2.9.0 - Notifications & Alerts

Phase 2.9.0 introduces the shared ACEMD Notification Service, Notifications workspace, alert lifecycle actions, local/dashboard delivery, and alert rules based on Health, Metrics, Automation, and critical Events. External channels are framework placeholders only in this phase.

## Phase 2.9.1 - Workspace & Navigation Framework

Phase 2.9.1 reorganizes ACEMD around permanent top-level workspaces before Phase 3 begins. Dashboard, Operations, Monitoring, Administration, Tools, and About become the stable navigation bank. Existing modules move into workspace secondary navigation without changing their URLs.
