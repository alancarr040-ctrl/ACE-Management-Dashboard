# ACE Management Dashboard Vision

## Product name

The official product name is **ACE Management Dashboard**.

The approved short name is **ACEMD**.

ACEMD is a management platform for ACE server operators. It is not ACE itself, and it is not a fork of the ACE emulator. ACE remains the emulator/server project. ACEMD surrounds ACE with operational, administrative, monitoring, automation, and future AI-assisted tooling.

## Mission

ACE Management Dashboard exists to make running an ACE server safer, clearer, and easier to maintain.

The project should help an operator answer four questions quickly:

1. Is my ACE server stack healthy?
2. What changed recently?
3. What can I safely do from the dashboard?
4. Where do I go to administer accounts, characters, players, and server data?

## Product philosophy

ACEMD should remain focused and operator-friendly.

The dashboard should not become a cluttered clone of Portainer, Cockpit, Webmin, or a generic server control panel. It should be an ACE-server-focused management dashboard with clear separation between current state, operational actions, historical events, automation, and future game administration modules.

## Core principles

### ACEMD is not ACE

Use **ACE** only when referring to the ACE emulator/server. Use **ACE Management Dashboard** or **ACEMD** when referring to this management platform.

### Manage through the wrapper

Operational actions should flow through `manage.sh` or a certified ACEMD service layer rather than embedding unrelated shell commands throughout the application.

### Health is read-only

The Health page answers what is happening. Corrective action belongs on the Management page or a future guided operations workflow.

### Events tell the story

Operationally meaningful changes should publish events. Events are the journal of what ACEMD observed or did.

### Grow functionality before growing the UI

New functionality should be integrated into existing subsystem views whenever practical. New cards or pages should represent distinct operational domains, not individual commands.

### One-screen operational summary

The primary operational dashboard should summarize the platform in one screen whenever practical. Detail should be available through drill-down pages rather than expanding the landing page vertically.

### Documentation is part of the product

Roadmap, governance, release notes, package documentation, and engineering decisions are part of the certified baseline.

## Why the project began with operations

The original goal includes account management, character management, login/session visibility, and administrative tools for ACE servers.

Those features are still core roadmap goals.

The project intentionally began by building the operational platform first because future administration modules need shared safety, health, logging, event, automation, and wrapper services. Building character or account tools before those foundations would force each module to solve infrastructure problems independently.

The 2.x series establishes that foundation. The 3.x series moves into ACE data and game administration.

## Long-term destination

The long-term destination is a complete ACE server administration platform that can manage:

- Infrastructure health.
- Operational tasks.
- Backups and recovery.
- Automation and scheduled maintenance.
- Accounts.
- Characters.
- Online players.
- Sessions and logins.
- World/runtime data.
- Database maintenance.
- Future AI-assisted diagnostics and recommendations.

ACEMD should make those capabilities available through safe, observable, documented, and auditable workflows.
