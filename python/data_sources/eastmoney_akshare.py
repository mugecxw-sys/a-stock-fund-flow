import time
from typing import Any

from core.normalize import normalize_moneyflow
from core.validate import validate_moneyflow


def fetch_moneyflow(max_attempts: int = 3, delay_seconds: int = 20) -> list[dict[str, Any]]:
    import akshare as ak

    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"请求东方财富概念资金流，第 {attempt} 次")
            df = ak.stock_sector_fund_flow_rank(
                indicator="今日",
                sector_type="概念资金流",
            )
            data = normalize_moneyflow(df)
            validate_moneyflow(data)
            return data
        except Exception as exc:
            last_error = exc
            print(f"东方财富请求失败: {type(exc).__name__}: {exc}")
            if attempt < max_attempts:
                time.sleep(delay_seconds * attempt)

    raise RuntimeError(f"东方财富数据源连续失败: {last_error}") from last_error
