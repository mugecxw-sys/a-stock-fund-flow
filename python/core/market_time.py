from datetime import datetime

from core.config import TIMEZONE, TRADING_WINDOWS


def now_beijing() -> datetime:
    return datetime.now(TIMEZONE)


def is_trading_window(moment: datetime) -> bool:
    if moment.weekday() >= 5:
        return False

    current_time = moment.time()
    return any(start <= current_time <= end for start, end in TRADING_WINDOWS)
