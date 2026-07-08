# ACEMD Project Specification

## Product

**ACE Management Dashboard** (**ACEMD**) is a web-based operations and administration platform for ACE server operators.

ACEMD is not the ACE emulator/server project. ACEMD manages, observes, automates, and eventually administers ACE server deployments.

## Scope

ACEMD includes:

- Dashboard UI.
- Management wrapper integration.
- Health checks.
- Operational events.
- Scheduler and automation framework.
- Metrics and notifications.
- Backup and recovery workflows.
- Future account, character, player, world, and database administration modules.

## Non-scope

ACEMD does not replace ACE and does not modify the emulator project identity. Any future ACE-specific data tools must be implemented as management/admin features around the server deployment, not as emulator forks.

## Current architecture layers

1. ACE emulator/server stack.
2. Host/container management wrapper.
3. ACEMD service layer.
4. ACEMD UI modules.
5. Future automation, metrics, notifications, and game administration modules.

## Certification expectation

Each future package should be built against the current accepted Git/ZIP baseline and should include release notes, package notes, and documentation updates.
