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
                i+1,
                "次"
            )


            df = ak.stock_sector_fund_flow_rank(
                indicator="今日",
                sector_type="概念资金流"
            )


            if df is not None and len(df)>0:

                return df


        except Exception as e:

            print(
                "失败:",
                e
            )


            time.sleep(15)



    return None




df = get_data()



if df is None:


    print(
        "获取失败，保持旧数据"
    )


    exit(0)




print(
    df.columns.tolist()
)



# ===================
# 找字段
# ===================


name_column=None

money_column=None



for col in df.columns:


    if "名称" in col:

        name_column=col


    if "主力净流入" in col:

        money_column=col




if name_column is None:

    raise Exception(
        "名称字段不存在"
    )



if money_column is None:

    raise Exception(
        "资金字段不存在"
    )




# ===================
# 数据处理
# ===================


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




# ===================
# 当前资金
# ===================


inflow=sorted(

    all_data,

    key=lambda x:x["money"],

    reverse=True

)[:10]



outflow=sorted(

    all_data,

    key=lambda x:x["money"]

)[:10]



now_data=inflow+outflow




now=datetime.now()



result={

    "update_time":

    now.strftime(
        "%Y-%m-%d %H:%M:%S"
    ),


    "data":

    now_data

}





# ===================
# 保存当前
# ===================


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





# ===================
# 保存小时历史
# ===================


folder_date=now.strftime(
    "%Y-%m-%d"
)


folder=f"history/{folder_date}"



os.makedirs(
    folder,
    exist_ok=True
)



file_time=now.strftime(
    "%H-%M"
)



with open(

    f"{folder}/{file_time}.json",

    "w",

    encoding="utf-8"

) as f:


    json.dump(

        result,

        f,

        ensure_ascii=False,

        indent=2

    )





# ===================
# 计算今日趋势
# ===================


trend={}



history_files=[]



for root,dirs,files in os.walk(
    "history"
):


    for file in files:

        if file.endswith(".json"):

            history_files.append(
                os.path.join(root,file)
            )




# 读取今天所有记录


for file in history_files:


    try:


        with open(

            file,

            "r",

            encoding="utf-8"

        ) as f:


            old=json.load(f)



        for item in old["data"]:


            name=item["name"]


            money=item["money"]


            if name not in trend:

                trend[name]=0



            trend[name]+=money



    except:

        pass




trend_list=[]



for k,v in trend.items():


    trend_list.append({

        "name":k,

        "money":round(v,2)

    })



trend_list=sorted(

    trend_list,

    key=lambda x:x["money"],

    reverse=True

)[:20]




trend_result={


    "update_time":

    now.strftime(
        "%Y-%m-%d %H:%M:%S"
    ),


    "data":

    trend_list


}



with open(

    "trend.json",

    "w",

    encoding="utf-8"

) as f:


    json.dump(

        trend_result,

        f,

        ensure_ascii=False,

        indent=2

    )



print(
    "当前资金更新完成"
)


print(
    "趋势数据更新完成"
)
