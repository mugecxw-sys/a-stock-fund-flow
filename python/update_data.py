import akshare as ak
import json
import time
import os
from datetime import datetime


def get_data():

    for i in range(3):

        try:

            print(
                "获取资金流，第",
                i + 1,
                "次"
            )


            df = ak.stock_sector_fund_flow_rank(
                indicator="今日",
                sector_type="概念资金流"
            )


            if df is not None and len(df) > 0:

                print("获取成功")

                return df


        except Exception as e:

            print(
                "失败:",
                e
            )


            time.sleep(15)



    return None



# =====================
# 获取数据
# =====================

df = get_data()



# =====================
# 获取失败
# 保留旧数据
# =====================

if df is None:


    print(
        "资金接口失败"
    )


    print(
        "保留已有数据"
    )


    exit(0)



print(
    df.columns.tolist()
)



# =====================
# 找字段
# =====================


name_column = None

money_column = None



for col in df.columns:


    if "名称" in col:

        name_column = col


    if "主力净流入" in col:

        money_column = col



if name_column is None:

    raise Exception(
        "没有名称字段"
    )



if money_column is None:

    raise Exception(
        "没有资金字段"
    )



# =====================
# 数据整理
# =====================


all_data=[]



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



    all_data.append({

        "name":name,

        "money":money

    })



# =====================
# 流入流出
# =====================


inflow=sorted(

    all_data,

    key=lambda x:x["money"],

    reverse=True

)[:10]



outflow=sorted(

    all_data,

    key=lambda x:x["money"]

)[:10]



result={


    "update_time":

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),


    "data":

        inflow+outflow

}



# =====================
# 保存最新
# =====================


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



# =====================
# 保存历史
# =====================


if not os.path.exists(
    "history"
):

    os.makedirs(
        "history"
    )



today=datetime.now().strftime(
    "%Y-%m-%d"
)



with open(

    f"history/{today}.json",

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
    "更新完成"
)
