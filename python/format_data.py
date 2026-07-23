def format_moneyflow(df):


    result=[]


    name_column=None

    money_column=None



    for col in df.columns:


        if "名称" in col:

            name_column=col


        if "主力净流入" in col:

            money_column=col



    if name_column is None:

        raise Exception(
            "找不到名称字段"
        )



    if money_column is None:

        raise Exception(
            "找不到资金字段"
        )



    for _,row in df.iterrows():


        try:

            money=float(
                row[money_column]
            )

        except:

            continue



        result.append({

            "name":
            row[name_column],


            "money":
            round(
                money/100000000,
                2
            )

        })


    return result
