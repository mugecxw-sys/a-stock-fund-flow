import json
from collections import defaultdict
from datetime import datetime
from typing import Any

from core.config import HISTORY_DIR


def append_snapshot(payload: dict[str, Any], now: datetime) -> None:
    history_file = HISTORY_DIR / f"{now:%Y-%m-%d}.jsonl"
    history_file.parent.mkdir(parents=True, exist_ok=True)

    with history_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False))
        file.write("\n")


def build_trend(now: datetime) -> dict[str, Any]:
    history_file = HISTORY_DIR / f"{now:%Y-%m-%d}.jsonl"
    snapshots = []

    if history_file.exists():
        with history_file.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    snapshots.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    first_values = {}
    latest_values = {}

    for snapshot in snapshots:
        for item in snapshot.get("data", []):
            name = item.get("name")
            money = item.get("money")
            if name is None or money is None:
                continue
            first_values.setdefault(name, money)
            latest_values[name] = money

    trend = []
    for name, latest_money in latest_values.items():
        first_money = first_values.get(name, latest_money)
        trend.append(
            {
                "name": name,
                "money": round(latest_money, 2),
                "change": round(latest_money - first_money, 2),
            }
        )

    trend.sort(key=lambda item: item["change"], reverse=True)

    return {
        "update_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "data": trend[:20],
    }
