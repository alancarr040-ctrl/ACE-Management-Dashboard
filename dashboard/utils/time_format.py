from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def parse_datetime(value: Any) -> datetime | None:
    """Parse ACEMD ISO-like timestamps into timezone-aware UTC datetimes."""
    if value in (None, "", "Never", "Pending", "None"):
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        if not text:
            return None
        try:
            if text.endswith("Z"):
                text = text[:-1] + "+00:00"
            dt = datetime.fromisoformat(text)
        except ValueError:
            for fmt in ("%Y-%m-%d %H:%M:%S UTC", "%Y-%m-%d %H:%M UTC", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    dt = datetime.strptime(text, fmt)
                    break
                except ValueError:
                    continue
            else:
                return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def absolute_time(value: Any) -> str:
    dt = parse_datetime(value)
    if not dt:
        return str(value) if value not in (None, "") else "Never"
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def relative_time(value: Any, now: datetime | None = None) -> str:
    dt = parse_datetime(value)
    if not dt:
        return str(value) if value not in (None, "") else "Never"
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    seconds = int((now - dt).total_seconds())
    if seconds < 0:
        return future_time(dt, now=now)
    if seconds < 5:
        return "just now"
    if seconds < 60:
        return f"{seconds} seconds ago"
    minutes = seconds // 60
    if minutes < 60:
        return _unit(minutes, "minute") + " ago"
    hours = minutes // 60
    if hours < 24:
        rem = minutes % 60
        if rem and hours < 6:
            return f"{_unit(hours, 'hour')} {_unit(rem, 'minute')} ago"
        return _unit(hours, "hour") + " ago"
    days = hours // 24
    if days == 1:
        return "yesterday"
    if days < 14:
        return _unit(days, "day") + " ago"
    weeks = days // 7
    if weeks < 8:
        return _unit(weeks, "week") + " ago"
    months = days // 30
    if months < 24:
        return _unit(months, "month") + " ago"
    years = days // 365
    return _unit(years, "year") + " ago"


def future_time(value: Any, now: datetime | None = None) -> str:
    dt = parse_datetime(value)
    if not dt:
        return str(value) if value not in (None, "") else "Pending"
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    seconds = int((dt - now).total_seconds())
    if seconds <= 0:
        return "due now"
    if seconds < 60:
        return f"in {seconds} seconds"
    minutes = seconds // 60
    if minutes < 60:
        return f"in {_unit(minutes, 'minute')}"
    hours = minutes // 60
    rem_minutes = minutes % 60
    if hours < 24:
        if rem_minutes:
            return f"in {_unit(hours, 'hour')} {_unit(rem_minutes, 'minute')}"
        return f"in {_unit(hours, 'hour')}"
    days = hours // 24
    rem_hours = hours % 24
    if days == 1 and rem_hours == 0:
        return "tomorrow"
    if days < 7:
        if rem_hours:
            return f"in {_unit(days, 'day')} {_unit(rem_hours, 'hour')}"
        return f"in {_unit(days, 'day')}"
    weeks = days // 7
    return f"in {_unit(weeks, 'week')}"


def time_display(value: Any, *, future: bool = False, now: datetime | None = None) -> dict[str, str]:
    if value in (None, ""):
        return {"relative": "Never" if not future else "Pending", "absolute": ""}
    return {
        "relative": future_time(value, now=now) if future else relative_time(value, now=now),
        "absolute": absolute_time(value),
    }


def _unit(value: int, label: str) -> str:
    return f"{value} {label}{'' if value == 1 else 's'}"
