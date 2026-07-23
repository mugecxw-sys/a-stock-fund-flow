import akshare as ak
import json
from datetime import datetime


df = ak.stock_sector_fund_flow_rank(
    indicator="今日",
    sector_type="概念资金流"
)


print(df.columns.tolist())


name_column = None

for col in df.columns:

    if "名称" in col:

        name_column = col

        break



money_column = None

for col in df.columns:

    if "主力净流入" in col:

        money_column = col

        break



if name_column is None:

    raise Exception("没有名称字段")


if money_column is None:

    raise Exception("没有资金字段")



data=[]


for _,row in df.iterrows():

    name=row[name_column]


    money=row[money_column]


    try:

        money=float(money)

    except:

        money=0



    money=round(
        money/100000000,
        2
    )


    data.append({

        "name":name,

        "money":money

    })



# 按资金排序

# 流入10个

inflow = sorted(
    data,
    key=lambda x:x["money"],
    reverse=True
)[:10]


# 流出10个

outflow = sorted(
    data,
    key=lambda x:x["money"]
)[:10]



result={


    "update_time":
    datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),


    "data":
    inflow + outflow


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



print("更新完成")
