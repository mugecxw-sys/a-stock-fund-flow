import sys
from datetime import timedelta
from pathlib import Path
from typing import Any


PYTHON_DIR = Path(__file__).resolve().parents[1]
if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))

from core.config import (  # noqa: E402
    LATEST_FILE,
    LEGACY_LATEST_FILE,
    SOURCE_CACHE_FILE,
    STALE_AFTER_HOURS,
    STATUS_FILE,
    TREND_FILE,
)
from core.market_time import is_trading_window, now_beijing  # noqa: E402
from core.normalize import build_top_list  # noqa: E402
from data_sources.eastmoney_akshare import fetch_moneyflow  # noqa: E402
from storage.cache_store import is_cache_fresh, load_cache, parse_time, save_cache  # noqa: E402
from storage.history_store import append_snapshot, build_trend  # noqa: E402
from storage.json_store import load_json, write_json  # noqa: E402


def _latest_from_payload(payload: dict[str, Any], now) -> dict[str, Any]:
    return {
        "update_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "source": payload.get("source", "eastmoney_akshare"),
        "fetched_at": payload.get("fetched_at"),
        "data": build_top_list(payload["data"]),
    }


def _status(
    state: str,
    now,
    last_success_time: str | None,
    message: str,
    error_type: str | None = None,
) -> dict[str, Any]:
    return {
        "state": state,
        "last_attempt_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "last_success_time": last_success_time,
        "source": "eastmoney_akshare",
        "error_type": error_type,
        "message": message,
    }


def _write_outputs(
    latest: dict[str, Any],
    status: dict[str, Any],
    append_history: bool,
    now,
) -> None:
    write_json(LATEST_FILE, latest)
    write_json(LEGACY_LATEST_FILE, latest)
    write_json(STATUS_FILE, status)

    if append_history:
        append_snapshot(latest, now)
        write_json(TREND_FILE, build_trend(now))


def _is_stale(cache_payload: dict[str, Any] | None, now) -> bool:
    if not cache_payload or not cache_payload.get("fetched_at"):
        return True

    age = now - parse_time(cache_payload["fetched_at"])
    return age > timedelta(hours=STALE_AFTER_HOURS)


def run() -> int:
    now = now_beijing()
    cache_payload = load_cache()

    if cache_payload and is_cache_fresh(cache_payload, now):
        print(f"缓存未过期，跳过东方财富请求: {SOURCE_CACHE_FILE}")
        latest = _latest_from_payload(cache_payload, now)
        status = _status(
            "cached",
            now,
            cache_payload.get("fetched_at_display"),
            "使用未过期缓存，避免频繁请求东方财富",
        )
        _write_outputs(latest, status, False, now)
        return 0

    if cache_payload and not is_trading_window(now):
        print("当前不在交易时段，使用最近成功缓存")
        latest = _latest_from_payload(cache_payload, now)
        status = _status(
            "cached",
            now,
            cache_payload.get("fetched_at_display"),
            "非交易时段使用最近成功缓存",
        )
        _write_outputs(latest, status, False, now)
        return 0

    try:
        data = fetch_moneyflow()
        cache_payload = {
            "source": "eastmoney_akshare",
            "fetched_at": now.isoformat(),
            "fetched_at_display": now.strftime("%Y-%m-%d %H:%M:%S"),
            "data": data,
        }
        save_cache(cache_payload)

        latest = _latest_from_payload(cache_payload, now)
        status = _status(
            "ok",
            now,
            cache_payload["fetched_at_display"],
            "东方财富数据更新成功",
        )
        _write_outputs(latest, status, True, now)
        print("数据更新完成")
        return 0
    except Exception as exc:
        print(f"数据源失败，尝试降级: {type(exc).__name__}: {exc}")

        if cache_payload:
            latest = _latest_from_payload(cache_payload, now)
            state = "stale" if _is_stale(cache_payload, now) else "degraded"
            status = _status(
                state,
                now,
                cache_payload.get("fetched_at_display"),
                "东方财富请求失败，使用最近成功缓存",
                type(exc).__name__,
            )
            _write_outputs(latest, status, False, now)
            return 0

        existing_latest = load_json(LATEST_FILE) or load_json(LEGACY_LATEST_FILE)
        if existing_latest:
            status = _status(
                "stale",
                now,
                existing_latest.get("update_time"),
                "东方财富请求失败，且无采集缓存，保留页面旧数据",
                type(exc).__name__,
            )
            write_json(STATUS_FILE, status)
            return 0

        status = _status(
            "failed",
            now,
            None,
            "东方财富请求失败，且没有任何可用缓存",
            type(exc).__name__,
        )
        write_json(STATUS_FILE, status)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
