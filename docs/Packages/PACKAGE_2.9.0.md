# Package 2.9.0 - Notifications & Alerts

## Objective

Introduce ACEMD notification and alert infrastructure so operators can be informed when health state changes, automation jobs fail, metrics cross thresholds, backups become stale, or other important events occur.

## Implemented Scope

- Notification service foundation.
- Notification dashboard/workspace.
- Alert rules for Health, Events, Automation, and Metrics.
- Local dashboard notifications.
- Notification history.
- Severity model for info, warning, critical, and recovery events.
- Initial delivery abstraction for future email, Discord, Slack, and webhook integrations.
- Notification lifecycle events written to the existing Event Service.

## Constraints

- No external notifications are sent in this release.
- Notification rules use existing ACEMD services.
- The dashboard remains compact; detail lives on the Notifications page.
- Events remain the journal; Notifications are operator-facing attention items.

## SQL

No SQL migration required.
