# Notification Architecture

## Purpose

The Notification Service converts ACEMD operational state into operator-facing alerts.

It consumes existing shared services instead of duplicating checks:

- Health Service
- Metrics Service
- Automation Service
- Event Service

## Separation of Responsibilities

- Metrics describe resource values.
- Health determines whether the platform is operating acceptably.
- Events record what happened over time.
- Automation performs scheduled checks and actions.
- Notifications tell humans what needs attention.

## Lifecycle

Notifications use the following states:

- `new` — freshly created attention item.
- `active` — still present and updated by the evaluation pass.
- `acknowledged` — operator has seen the alert but it may not be fixed.
- `resolved` — alert no longer needs attention.

When a monitored condition clears, the Notification Service can auto-resolve the active notification.

## Persistence

The initial implementation stores notifications in the ACEMD runtime directory as JSON. This avoids a database migration and keeps Phase 2.9.0 deployable in the same style as Events and Automation state.

Default path:

`/opt/acserver/backups/runtime/notifications.json`

Override:

`ACEMD_NOTIFICATIONS_STATE`

## Channels

2.9.0 includes a channel registry but only enables local dashboard delivery. Future packages may add configured outbound channels after delivery policy, retry behavior, and secret handling are defined.
