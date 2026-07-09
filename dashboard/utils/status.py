from __future__ import annotations


def severity_badge_class(level: str | None) -> str:
    normalized = (level or "").lower()
    if normalized in {"ok", "info", "healthy", "success", "running"}:
        return "green"
    if normalized in {"warning", "warn", "starting", "degraded"}:
        return "yellow"
    if normalized in {"critical", "error", "failed", "unhealthy", "stopped"}:
        return "red"
    return "gray"


def health_hero_level(level: str | None) -> str:
    normalized = (level or "").lower()
    if normalized in {"ok", "info", "healthy", "success"}:
        return "ok"
    if normalized in {"warning", "warn", "starting", "degraded"}:
        return "warning"
    if normalized in {"critical", "error", "failed", "unhealthy"}:
        return "critical"
    return "unknown"
