from datetime import datetime
from typing import Any

from app.config import settings


def prioritize_data(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not data:
        return data

    if "created_at" in data[0]:
        return sorted(data, key=lambda row: row.get("created_at", ""), reverse=True)
    if "date" in data[0]:
        return sorted(data, key=lambda row: row.get("date", ""), reverse=True)
    return data


def paginate(data: list[dict[str, Any]], page: int, page_size: int) -> list[dict[str, Any]]:
    start = (page - 1) * page_size
    end = start + page_size
    return data[start:end]


def apply_voice_limits(limit: int, voice_mode: bool) -> int:
    if voice_mode:
        return min(limit, settings.default_voice_limit)
    return min(limit, settings.max_limit)


def freshness_label(data: list[dict[str, Any]]) -> str:
    if not data:
        return "No data available"

    candidate = data[0].get("created_at") or data[0].get("date")
    if not candidate:
        return "Freshness unavailable"

    try:
        observed_time = datetime.fromisoformat(str(candidate).replace("Z", ""))
    except ValueError:
        return "Freshness unavailable"

    delta = datetime.utcnow() - observed_time
    if delta.days > 0:
        return f"Data as of {delta.days} day(s) ago"

    hours = max(int(delta.total_seconds() // 3600), 0)
    return f"Data as of {hours} hour(s) ago"
