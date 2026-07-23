import akshare as ak
import json
import time
from datetime import datetime


# ==========================
# 获取资金流数据（带重试）
# ==========================

df = None


for i in range(3):

    try:

        print("正在获取资金流，第", i+1, "次")

        df = ak.stock_sector_fund_flow_rank(
            indicator="今日",
            sector_type="概念资金流"
        )


        if df is not None and len(df) > 0:

            print("获取成功")

            break


    except Exception as e:

        print("获取失败：", e)

        time.sleep(10)



if df is None or len(df) == 0:

    raise Exception(
        "AKShare获取数据失败"
    )



print("字段：")

print(df.columns.tolist())



# ==========================
# 自动寻找字段
# ==========================


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

    raise Exception(
        "没有找到板块名称字段"
    )


if money_column is None:

    raise Exception(
        "没有找到主力资金字段"
    )



# ==========================
# 数据整理
# ==========================


all_data = []


for _, row in df.iterrows():


    name = row[name_column]


    money = row[money_column]


    try:

        money = float(money)


    except:


        # 如果是字符串，例如：
        # 12.5亿

        money = 0



    money = round(
        money / 100000000,
        2
    )


    all_data.append(

        {

            "name": name,

            "money": money

        }

    )



# ==========================
# 资金流入10个
# ==========================


inflow = sorted(

    all_data,

    key=lambda x:x["money"],

    reverse=True

)[:10]



# ==========================
# 资金流出10个
# ==========================


outflow = sorted(

    all_data,

    key=lambda x:x["money"]

)[:10]



final_data = inflow + outflow



# ==========================
# 保存JSON
# ==========================


result = {


    "update_time":

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),


    "data": final_data


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



print(
    "资金流更新完成，共",
    len(final_data),
    "个板块"
)
