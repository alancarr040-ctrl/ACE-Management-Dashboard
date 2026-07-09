# ACE Management Dashboard Roadmap

## Product identity

**Product name:** ACE Management Dashboard  
**Short name:** ACEMD

ACEMD is a companion management and administration platform for the ACE emulator/server stack. ACEMD is not a fork of ACE and is not intended to replace ACE. The term **ACE** refers to the underlying emulator/server project. The terms **ACE Management Dashboard** and **ACEMD** refer to this dashboard, wrapper, automation, monitoring, and administration platform.

## Vision

ACE Management Dashboard is intended to become a complete web-based administration platform for running and maintaining an ACE server.

The long-term vision includes:

- Operational health monitoring.
- Controlled management actions through a wrapper.
- Event history and operational journaling.
- Scheduler and automation services.
- Resource metrics and alerting.
- ACE account administration.
- ACE character administration.
- Online player and session visibility.
- World and database administration tools.
- Future AI-assisted operational diagnostics.

## Why operations came first

The project began with operational infrastructure because all later administration features depend on a safe, observable, and repeatable platform.

Account, character, and player tools should not each implement their own Docker calls, health checks, logging, event publishing, database safety checks, or recovery behavior. Those concerns belong to ACEMD core services.

The current 2.x phases establish the platform layer. Beginning with the 3.x series, development shifts toward the original game administration vision: accounts, characters, players, world management, and database tools.

## Roadmap overview

| Phase | Name | Status | Purpose |
|---|---|---:|---|
| 2.3.x | Management Wrapper | Complete | Standardized command-line management interface. |
| 2.4.x | Interactive Management | Complete | Web operations console backed by the wrapper. |
| 2.5.x | Operational Health | Complete | Read-only health dashboard and service checks. |
| 2.6.0 | Operational Monitoring & Events | Complete | Event journal and health transition tracking. |
| 2.6.1 | Roadmap & Vision | Complete | Public roadmap, product identity, and project direction. |
| 2.7.0 | Scheduler & Automation | Complete | Background job framework and automation foundation. |
| 2.7.1 | Repository & Documentation Reorganization | Complete | Clean documentation layout and root directory policy. |
| 2.7.2 | Automation Framework & UI Polish | Complete | Job registry foundation, shared time formatting, and UI consistency. |
| 2.8.0 | Metrics & Resource Monitoring | Complete | CPU, memory, disk, network, and container resource views. |
| 2.9.0 | Notifications & Alerts | Complete | Notification service, alert lifecycle, and local/dashboard operator alerts. |
| 2.9.1 | Workspace & Navigation Framework | Complete | Compact workspace navigation before Phase 3 administration modules. |
| 3.0.1 | ACE Schema Discovery | Current Development | Safe read-only ACE schema discovery and explorer foundation. |
| 3.1.0 | Account Management | Planned | View and manage ACE accounts through ACEMD. |
| 3.2.0 | Character Management | Planned | View and manage ACE characters through ACEMD. |
| 3.3.0 | Online Player Management | Planned | Session visibility, online player status, and operator tools. |
| 3.4.0 | World Administration | Planned | World/runtime views and safe administration workflows. |
| 3.5.0 | Database Administration | Planned | Database inspection, maintenance helpers, and guarded administrative actions. |
| 4.x | Advanced Platform | Future | AI operations assistant, plugins, multi-server management, and advanced automation. |

## Platform foundation track

### 2.3.x - Management Wrapper

Standardize host and container management through `manage.sh`. The wrapper is the supported operational interface for ACEMD-managed actions.

### 2.4.x - Interactive Management

Expose approved wrapper actions through the Management page using a compact, whitelisted, operator-safe interface.

### 2.5.x - Operational Health

Provide a compact one-screen answer to the question: "Is the ACEMD-managed ACE stack healthy?"

### 2.6.x - Operational Events

Track meaningful operational changes over time. Health, management, automation, backup, and future subsystems should publish events through a shared event service.

### 2.7.0 - Scheduler & Automation

Introduce the ACEMD Automation Engine, Automation dashboard, request-driven scheduler, built-in read-only jobs, manual job runs, job history, and event publishing.

### 2.7.1 - Repository & Documentation Reorganization

Reorganize repository documentation so package notes, release notes, vision, operational docs, development standards, and engineering decision records live under logical `docs/` directories while the repository root remains clean.

### 2.7.2 - Automation Framework & UI Polish

Refine the Automation Engine with a registry-backed job model and shared UI helpers for relative time, muted absolute timestamps, and consistent severity presentation.

### 2.8.0 - Metrics & Resource Monitoring

Add system and container metrics to help explain why a service is unhealthy or under load. Phase 2.8.0 introduces the shared Metrics Service, Metrics workspace, metrics API, threshold checks, and Metrics Snapshot automation job.

### 2.9.0 - Notifications & Alerts

Notify operators when health changes, jobs fail, backups become stale, disk usage crosses thresholds, or other important events occur.

### 2.9.1 - Workspace & Navigation Framework

Reorganize ACEMD around permanent top-level workspaces: Dashboard, Operations, Monitoring, Administration, Tools, and About. Existing Phase 2 modules remain available as workspace modules while Phase 3 administration gains a dedicated home.

## ACE administration track

The 3.x roadmap returns to the original administration goals of the project.

### 3.0.0 - ACE Data Integration Foundation

Create safe, documented, read-only access patterns for ACE database and runtime data. This phase should avoid destructive administration features until the data model, permissions, and safety rules are certified.

### 3.1.0 - Account Management

Add account visibility and administration workflows.

### 3.2.0 - Character Management

Add character search, profile views, character metadata, and carefully guarded administrative actions.

### 3.3.0 - Online Player Management

Add online player/session visibility, runtime status, and operator-facing tools.

### 3.4.0 - World Administration

Add world and runtime views that help operators understand the ACE server state.

### 3.5.0 - Database Administration

Add database-oriented tools using ACEMD safety patterns, audit trails, and event publishing.

## Advanced platform track

The 4.x series is reserved for advanced capabilities after the platform and game administration layers are stable.

Potential areas include:

- AI-assisted operations.
- Plugin framework.
- Multi-server support.
- Cluster management.
- Advanced audit and compliance tools.
- Expanded automation and remediation workflows.

## Roadmap governance

The roadmap is part of the certified project baseline. Future packages should update this file whenever a phase is completed, renamed, deferred, added, or materially changed.

Detailed implementation planning may live in `docs/AI/AI_ROADMAP.md` and `docs/Packages/`, but this root `ROADMAP.md` is the public GitHub-facing roadmap.
