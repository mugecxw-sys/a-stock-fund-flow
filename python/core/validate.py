from core.config import MIN_VALID_ROWS


def validate_moneyflow(data: list[dict]) -> None:
    if len(data) < MIN_VALID_ROWS:
        raise ValueError(f"有效数据不足: {len(data)} < {MIN_VALID_ROWS}")

    positive_count = sum(1 for item in data if item["money"] > 0)
    negative_count = sum(1 for item in data if item["money"] < 0)

    if positive_count == 0:
        raise ValueError("没有资金流入数据")

    if negative_count == 0:
        raise ValueError("没有资金流出数据")

    names = [item["name"] for item in data]
    if len(names) != len(set(names)):
        raise ValueError("板块名称存在重复")
