import akshare as ak


def get_data():


    df = ak.stock_sector_fund_flow_summary()


    if df is None or len(df)==0:

        raise Exception(
            "备用接口返回为空"
        )


    return df
