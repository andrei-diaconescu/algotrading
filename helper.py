import pandas as pd
from pandas import DataFrame
from algotrading.trade import Trade


def trades_to_dataframe(trades: list[Trade]) -> DataFrame:
    trades_df = DataFrame()
    for i, trade in enumerate(trades):
        frame = DataFrame(trade.to_dict(), index=[i + 1])
        trades_df = pd.concat([trades_df, frame])
    return trades_df
