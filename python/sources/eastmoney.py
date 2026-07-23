import akshare as ak


def get_data():


    df = ak.stock_sector_fund_flow_rank(
        indicator="今日",
        sector_type="概念资金流"
    )


    if df is None or len(df)==0:

        raise Exception(
            "东方财富主接口为空"
        )


    return df
