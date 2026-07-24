from datetime import datetime, timedelta
from typing import Any

from core.config import CACHE_TTL_MINUTES, SOURCE_CACHE_FILE, TIMEZONE
from storage.json_store import load_json, write_json


def load_cache() -> dict[str, Any] | None:
    return load_json(SOURCE_CACHE_FILE)


def save_cache(payload: dict[str, Any]) -> None:
    write_json(SOURCE_CACHE_FILE, payload)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value).astimezone(TIMEZONE)


def is_cache_fresh(payload: dict[str, Any], now: datetime) -> bool:
    fetched_at = payload.get("fetched_at")
    if not fetched_at:
        return False

    age = now - parse_time(fetched_at)
    return timedelta(0) <= age <= timedelta(minutes=CACHE_TTL_MINUTES)
