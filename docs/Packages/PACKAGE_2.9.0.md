# Package 2.9.0 - Notifications & Alerts

## Objective

Introduce ACEMD notification and alert infrastructure so operators can be informed when health state changes, automation jobs fail, metrics cross thresholds, backups become stale, or other important events occur.

## Planned Scope

- Notification service foundation.
- Notification dashboard/workspace.
- Alert rules for Health, Events, Automation, and Metrics.
- Local dashboard notifications.
- Notification history.
- Severity model for info, warning, critical, and recovery events.
- Initial delivery abstraction for future email, Discord, Slack, and webhook integrations.

## Constraints

- Do not send external notifications until delivery configuration and safety rules are documented.
- Keep alert rules compact and operator-readable.
- Use existing ACEMD services instead of duplicating health, event, automation, or metric logic.
- Maintain the distinction between Events as the journal and Notifications as operator-facing attention items.

## Documentation Requirements

- Update `ROADMAP.md` and `docs/AI/AI_ROADMAP.md`.
- Add notification architecture documentation.
- Add release notes and package README.
- Define how future ACE administration modules should publish notification-worthy events.
