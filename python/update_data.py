import json
import os
from datetime import datetime


from sources import eastmoney
from sources import em_backup

from format_data import format_moneyflow



# ======================
# 获取数据
# ======================


def get_moneyflow():


    # 第一接口

    try:

        print(
            "尝试东方财富主接口"
        )


        df = eastmoney.get_data()


        data = format_moneyflow(df)


        if len(data)>0:

            print(
                "东方财富成功"
            )


            return data



    except Exception as e:


        print(
            "东方财富失败:",
            e
        )




    # 第二接口

    try:

        print(
            "尝试备用接口"
        )


        df = em_backup.get_data()


        data = format_moneyflow(df)


        if len(data)>0:


            print(
                "备用接口成功"
            )


            return data



    except Exception as e:


        print(
            "备用接口失败:",
            e
        )




    return None





# ======================
# 主程序
# ======================


data = get_moneyflow()



if data is None:


    print(
        "所有数据源失败"
    )


    print(
        "保持旧数据"
    )


    exit(0)




# ======================
# TOP10
# ======================


inflow = sorted(

    data,

    key=lambda x:x["money"],

    reverse=True

)[:10]



outflow = sorted(

    data,

    key=lambda x:x["money"]

)[:10]



final_data = inflow + outflow





now=datetime.now()



result={


    "update_time":

    now.strftime(
        "%Y-%m-%d %H:%M:%S"
    ),


    "data":

    final_data

}





# ======================
# 保存最新数据
# ======================


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





# ======================
# 保存小时历史
# ======================


folder = (

    "history/"
    +
    now.strftime("%Y-%m-%d")

)



os.makedirs(

    folder,

    exist_ok=True

)



filename = now.strftime(
    "%H-%M.json"
)



with open(

    f"{folder}/{filename}",

    "w",

    encoding="utf-8"

) as f:


    json.dump(

        result,

        f,

        ensure_ascii=False,

        indent=2

    )





# ======================
# 生成trend
# ======================


trend={}



for root,dirs,files in os.walk(
    "history"
):


    for file in files:


        if file.endswith(".json"):


            try:


                with open(

                    os.path.join(root,file),

                    "r",

                    encoding="utf-8"

                ) as f:


                    old=json.load(f)



                for item in old["data"]:


                    name=item["name"]


                    money=item["money"]



                    trend[name]=(

                        trend.get(name,0)

                        +

                        money

                    )



            except:


                pass




trend_data=[]



for k,v in trend.items():


    trend_data.append({

        "name":k,

        "money":round(v,2)

    })



trend_data=sorted(

    trend_data,

    key=lambda x:x["money"],

    reverse=True

)[:20]





with open(

    "trend.json",

    "w",

    encoding="utf-8"

) as f:


    json.dump(

        {

        "update_time":
        now.strftime(
        "%Y-%m-%d %H:%M:%S"
        ),

        "data":
        trend_data

        },

        f,

        ensure_ascii=False,

        indent=2

    )




print(
    "全部更新完成"
)
