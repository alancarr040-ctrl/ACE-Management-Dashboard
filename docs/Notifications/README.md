# Notifications & Alerts

Phase 2.9.0 introduces the ACEMD notification layer.

Events remain the chronological operational journal. Notifications are the smaller operator-facing set of attention items derived from Health, Metrics, Automation, and Events.

## Initial Scope

- Local dashboard notification center.
- Active alert summary.
- Notification lifecycle: new, active, acknowledged, resolved.
- Health-derived alerts.
- Metrics threshold alerts.
- Automation warning alerts.
- Critical event surfacing.
- Channel framework for future delivery providers.

## Delivery Channels

2.9.0 enables local/dashboard notification delivery only.

External delivery channels such as email, Discord, Slack, and generic webhooks are intentionally deferred until configuration, safety, and retry rules are documented.
