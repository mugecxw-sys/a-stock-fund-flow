import akshare as ak
import json
from datetime import datetime


# 获取东方财富概念板块资金流

df = ak.stock_sector_fund_flow_rank(
    indicator="今日",
    sector_type="概念资金流"
)
print(df.columns.tolist())

# 按主力净流入排序
# 取前20个

df = df.head(20)


data = []


for _, row in df.iterrows():

    name = row["名称"]

    # 自动寻找资金字段

money_column = None

for col in df.columns:

    if "主力净流入" in col:
        money_column = col
        break


if money_column is None:
    raise Exception(
        "没有找到主力资金字段，请检查AKShare返回数据"
    )


money = row[money_column]


    # 单位转换：
    # 元 -> 亿

    money = round(
        float(money) / 100000000,
        2
    )


    data.append(
        {
            "name": name,
            "money": money
        }
    )



result = {

    "update_time":
    datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),

    "data":data

}


with open(
    "moneyflow.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )


print("资金流更新完成")
