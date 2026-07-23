import akshare as ak


def get_data():

    df = ak.stock_sector_fund_flow_summary_em()


    if df is None or len(df)==0:

        raise Exception(
            "备用资金接口为空"
        )


    return df
