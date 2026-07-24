import math
from typing import Any


def _find_name_column(columns: list[str]) -> str:
    for column in columns:
        if "名称" in column:
            return column
    raise ValueError("找不到名称字段")


def _find_money_column(columns: list[str]) -> str:
    preferred = [
        "今日主力净流入-净额",
        "主力净流入-净额",
    ]

    for column in preferred:
        if column in columns:
            return column

    for column in columns:
        if "主力净流入" in column and "净额" in column:
            return column

    for column in columns:
        if "主力净流入" in column:
            return column

    raise ValueError("找不到资金字段")


def _to_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if math.isnan(number) or math.isinf(number):
        return None

    return number


def normalize_moneyflow(df) -> list[dict[str, Any]]:
    columns = [str(column) for column in df.columns]
    name_column = _find_name_column(columns)
    money_column = _find_money_column(columns)

    result = []
    for _, row in df.iterrows():
        money = _to_float(row[money_column])
        name = str(row[name_column]).strip()

        if money is None or not name or name.lower() == "nan":
            continue

        result.append(
            {
                "name": name,
                "money": round(money / 100000000, 2),
            }
        )

    return result


def build_top_list(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    inflow = sorted(data, key=lambda item: item["money"], reverse=True)[:10]
    outflow = sorted(data, key=lambda item: item["money"])[:10]
    return inflow + outflow
