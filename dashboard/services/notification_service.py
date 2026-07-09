from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from utils.status import severity_badge_class
from utils.time_format import time_display


class NotificationService:
    """Operator-facing alert and notification layer for ACEMD.

    Events remain the historical journal. Notifications are the smaller set of
    active attention items derived from Health, Metrics, Automation, and Events.
    Phase 2.9.0 intentionally ships with local/dashboard delivery only; external
    channels are framework placeholders for later safely-configured packages.
    """

    ACTIVE_STATES = {"new", "active"}
    CLOSED_STATES = {"acknowledged", "resolved"}

    def __init__(self, health_service, metrics_service, automation_service, event_service, root_path: str | Path | None = None):
        self.health_service = health_service
        self.metrics_service = metrics_service
        self.automation_service = automation_service
        self.event_service = event_service
        self.root_path = Path(root_path or os.environ.get("ACE_ROOT", "/opt/acserver")).resolve()
        runtime_dir = Path(os.environ.get("ACE_RUNTIME_DIR", self.root_path / "backups" / "runtime"))
        self.state_path = Path(os.environ.get("ACEMD_NOTIFICATIONS_STATE", runtime_dir / "notifications.json"))
        self.max_notifications = int(os.environ.get("ACEMD_NOTIFICATIONS_MAX", "300"))
        self.channels = [
            {"id": "dashboard", "name": "Dashboard", "enabled": True, "status": "Active", "detail": "Local ACEMD notification workspace and summary badge."},
            {"id": "event_journal", "name": "Event Journal", "enabled": True, "status": "Active", "detail": "Notification lifecycle changes are recorded as operational events."},
            {"id": "email", "name": "Email", "enabled": False, "status": "Deferred", "detail": "Reserved for a future configured delivery package."},
            {"id": "webhook", "name": "Webhook", "enabled": False, "status": "Deferred", "detail": "Reserved for future Discord, Slack, and generic webhook delivery."},
        ]

    def get_center(self, refresh: bool = True) -> dict[str, Any]:
        if refresh:
            self.evaluate()
        notifications = self._read()
        active = [n for n in notifications if n.get("state") in self.ACTIVE_STATES]
        history = list(reversed(notifications[-self.max_notifications:]))
        summary = self._summary(notifications)
        return {
            "overall": self._overall(summary),
            "summary": summary,
            "active": [self._view(n) for n in sorted(active, key=lambda r: (self._severity_weight(r.get("severity")), r.get("updated_at", "")), reverse=True)],
            "history": [self._view(n) for n in history[:100]],
            "channels": self.channels,
            "rules": self._rules(),
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }

    def evaluate(self) -> list[dict[str, Any]]:
        desired = []
        desired.extend(self._from_health())
        desired.extend(self._from_metrics())
        desired.extend(self._from_automation())
        desired.extend(self._from_events())
        return self._reconcile(desired)

    def acknowledge(self, notification_id: str) -> bool:
        return self._transition(notification_id, "acknowledged", "Notification acknowledged")

    def resolve(self, notification_id: str) -> bool:
        return self._transition(notification_id, "resolved", "Notification resolved")

    def _from_health(self) -> list[dict[str, Any]]:
        health = self._safe(self.health_service.get_health, {})
        rows = []
        overall = health.get("overall", {}) if isinstance(health, dict) else {}
        if overall.get("level") in {"warning", "critical"}:
            rows.append(self._desired(
                key="health:overall",
                source="health",
                severity=overall.get("level", "warning"),
                title=f"Operational health is {overall.get('label', 'degraded')}",
                message=overall.get("message", "Operational health requires review."),
                entity="ACEMD Health",
            ))
        for check in (health.get("checks", []) if isinstance(health, dict) else []):
            if check.get("level") in {"warning", "critical"}:
                rows.append(self._desired(
                    key=f"health:check:{check.get('name')}",
                    source="health",
                    severity=check.get("level", "warning"),
                    title=f"Health check: {check.get('name')}",
                    message=f"{check.get('status', 'Review required')} — {check.get('detail', '')}",
                    entity=check.get("name", "Health Check"),
                ))
        return rows

    def _from_metrics(self) -> list[dict[str, Any]]:
        metrics = self._safe(self.metrics_service.get_metrics, {})
        rows = []
        for check in (metrics.get("checks", []) if isinstance(metrics, dict) else []):
            if check.get("level") in {"warning", "critical"}:
                rows.append(self._desired(
                    key=f"metrics:threshold:{check.get('name')}",
                    source="metrics",
                    severity=check.get("level", "warning"),
                    title=f"Metric threshold: {check.get('name')}",
                    message=f"{check.get('status', 'Threshold crossed')} — {check.get('detail', '')}",
                    entity=check.get("name", "Metric"),
                ))
        return rows

    def _from_automation(self) -> list[dict[str, Any]]:
        automation = self._safe(lambda: self.automation_service.get_status(run_due=False), {})
        engine = automation.get("engine", {}) if isinstance(automation, dict) else {}
        rows = []
        if engine.get("failures", 0):
            rows.append(self._desired(
                key="automation:failures",
                source="automation",
                severity="warning",
                title="Automation jobs require review",
                message=f"{engine.get('failures')} automation job warning(s) were reported.",
                entity="Automation Engine",
            ))
        for job in (automation.get("jobs", []) if isinstance(automation, dict) else []):
            badge = job.get("last_result_badge") or "green"
            if badge in {"yellow", "red"} or str(job.get("last_result", "")).lower() in {"warning", "failed", "critical"}:
                rows.append(self._desired(
                    key=f"automation:job:{job.get('id')}",
                    source="automation",
                    severity="critical" if badge == "red" else "warning",
                    title=f"Automation job: {job.get('name')}",
                    message=job.get("last_detail", "Automation job requires review."),
                    entity=job.get("name", "Automation Job"),
                ))
        return rows

    def _from_events(self) -> list[dict[str, Any]]:
        rows = []
        summary = self._safe(self.event_service.get_summary, {})
        latest = summary.get("latest") if isinstance(summary, dict) else None
        if latest and latest.get("severity") == "critical":
            rows.append(self._desired(
                key=f"events:latest-critical:{latest.get('entity')}:{latest.get('type')}",
                source="events",
                severity="critical",
                title=f"Critical event: {latest.get('title')}",
                message=latest.get("message", "A critical operational event was recorded."),
                entity=latest.get("entity", "Event Journal"),
            ))
        return rows

    def _reconcile(self, desired: list[dict[str, Any]]) -> list[dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        existing = self._read()
        by_key = {n.get("key"): n for n in existing if n.get("key")}
        desired_keys = {d["key"] for d in desired}
        changed: list[dict[str, Any]] = []

        for row in desired:
            current = by_key.get(row["key"])
            if not current or current.get("state") == "resolved":
                notice = {**row, "id": self._id(row["key"]), "state": "new", "created_at": now, "updated_at": now, "count": 1, "channels": ["dashboard"]}
                existing.append(notice)
                changed.append(notice)
                self._record_lifecycle(notice, "created")
            else:
                if any(current.get(k) != row.get(k) for k in ["severity", "title", "message", "entity"]):
                    previous_state = current.get("state", "active")
                    current.update(row)
                    current["updated_at"] = now
                    current["state"] = previous_state if previous_state == "acknowledged" else "active"
                    current["count"] = int(current.get("count", 1) or 1) + 1
                    changed.append(current)

        for current in existing:
            if current.get("state") in self.ACTIVE_STATES and current.get("key") not in desired_keys:
                current["state"] = "resolved"
                current["updated_at"] = now
                changed.append(current)
                self._record_lifecycle(current, "auto_resolved")

        existing = existing[-self.max_notifications:]
        self._write(existing)
        return [self._view(n) for n in changed]

    def _transition(self, notification_id: str, state: str, title: str) -> bool:
        rows = self._read()
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for row in rows:
            if row.get("id") == notification_id:
                row["state"] = state
                row["updated_at"] = now
                self._write(rows)
                self._record_lifecycle(row, state, title=title)
                return True
        return False

    def _record_lifecycle(self, notice: dict[str, Any], action: str, title: str | None = None) -> None:
        try:
            self.event_service.record_event(
                source="notifications",
                event_type=f"notification_{action}",
                severity="info" if action in {"acknowledged", "resolved", "auto_resolved"} else notice.get("severity", "info"),
                title=title or f"Notification {action.replace('_', ' ')}",
                message=notice.get("message", ""),
                entity=notice.get("entity", "Notification"),
                current=notice.get("state"),
                metadata={"notification_id": notice.get("id"), "key": notice.get("key")},
            )
        except Exception:
            pass

    def _desired(self, *, key: str, source: str, severity: str, title: str, message: str, entity: str) -> dict[str, Any]:
        return {"key": key, "source": source, "severity": severity if severity in {"info", "ok", "warning", "critical"} else "warning", "title": title, "message": message, "entity": entity}

    def _summary(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        active = [n for n in rows if n.get("state") in self.ACTIVE_STATES]
        return {
            "total": len(rows),
            "active": len(active),
            "critical": sum(1 for n in active if n.get("severity") == "critical"),
            "warning": sum(1 for n in active if n.get("severity") == "warning"),
            "info": sum(1 for n in active if n.get("severity") in {"info", "ok"}),
            "acknowledged": sum(1 for n in rows if n.get("state") == "acknowledged"),
            "resolved": sum(1 for n in rows if n.get("state") == "resolved"),
        }

    def _overall(self, summary: dict[str, Any]) -> dict[str, str]:
        if summary.get("critical"):
            return {"level": "critical", "label": "Critical Alerts", "message": "One or more critical alerts need operator attention."}
        if summary.get("warning"):
            return {"level": "warning", "label": "Active Alerts", "message": "One or more alerts need review."}
        return {"level": "ok", "label": "Clear", "message": "No active operator notifications."}

    def _rules(self) -> list[dict[str, str]]:
        return [
            {"source": "Health", "name": "Health warnings and critical checks", "detail": "Creates alerts from degraded overall health and failed health checks."},
            {"source": "Metrics", "name": "Threshold warnings and criticals", "detail": "Creates alerts when resource threshold checks cross warning or critical levels."},
            {"source": "Automation", "name": "Automation job warnings", "detail": "Creates alerts when scheduler jobs report warning or failed status."},
            {"source": "Events", "name": "Latest critical event", "detail": "Surfaces the newest critical operational event as an operator alert."},
        ]

    def _view(self, row: dict[str, Any]) -> dict[str, Any]:
        view = dict(row)
        created = time_display(row.get("created_at"))
        updated = time_display(row.get("updated_at"))
        view["created_display"] = created
        view["updated_display"] = updated
        view["badge_class"] = severity_badge_class(row.get("severity"))
        view["state_badge"] = "green" if row.get("state") == "resolved" else "yellow" if row.get("state") == "acknowledged" else severity_badge_class(row.get("severity"))
        return view

    def _read(self) -> list[dict[str, Any]]:
        if not self.state_path.exists():
            return []
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _write(self, rows: list[dict[str, Any]]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    def _id(self, key: str) -> str:
        cleaned = "".join(ch if ch.isalnum() else "-" for ch in key.lower()).strip("-")
        return cleaned[:80] or "notification"

    def _severity_weight(self, severity: str | None) -> int:
        return {"critical": 4, "warning": 3, "info": 2, "ok": 1}.get(severity or "", 0)

    def _safe(self, fn, fallback):
        try:
            return fn()
        except Exception:
            return fallback
