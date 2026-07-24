import os
from datetime import time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT_DIR = Path(__file__).resolve().parents[2]
PYTHON_DIR = ROOT_DIR / "python"
DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
HISTORY_DIR = DATA_DIR / "history"

LEGACY_LATEST_FILE = ROOT_DIR / "moneyflow.json"
LATEST_FILE = DATA_DIR / "latest.json"
STATUS_FILE = DATA_DIR / "status.json"
TREND_FILE = DATA_DIR / "trend.json"
SOURCE_CACHE_FILE = CACHE_DIR / "eastmoney_latest.json"

try:
    TIMEZONE = ZoneInfo("Asia/Shanghai")
except ZoneInfoNotFoundError:
    TIMEZONE = timezone(timedelta(hours=8), name="Asia/Shanghai")
CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "50"))
STALE_AFTER_HOURS = int(os.getenv("STALE_AFTER_HOURS", "24"))
MIN_VALID_ROWS = int(os.getenv("MIN_VALID_ROWS", "20"))

TRADING_WINDOWS = (
    (time(9, 25), time(11, 35)),
    (time(12, 55), time(15, 10)),
)
