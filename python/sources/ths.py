import akshare as ak


def get_data():


    df = ak.stock_board_concept_name_ths()



    if df is None or len(df)==0:

        raise Exception(
            "同花顺概念为空"
        )


    return df
