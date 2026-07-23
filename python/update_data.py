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



if df is None:


    print(
        "资金接口失败，保持旧数据"
    )


    exit(0)



print(
    df.columns.tolist()
)



# =====================
# 字段识别
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
# 数据处理
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
# TOP10
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



data=inflow+outflow



# =====================
# 生成结果
# =====================


now=datetime.now()



result={


    "update_time":

        now.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),


    "data":

        data

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
# 保存小时历史
# =====================


date_folder = now.strftime(
    "%Y-%m-%d"
)


time_file = now.strftime(
    "%H-%M"
)



folder = f"history/{date_folder}"



if not os.path.exists(folder):

    os.makedirs(folder)



with open(

    f"{folder}/{time_file}.json",

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


print(
    "历史保存:",
    f"{folder}/{time_file}.json"
)
