from typing import List
import pandas as pd
from pandas import DataFrame
from algotrading.trade import Trade

M1 = "1m"
M3 = "3m"
M5 = "5m"
M15 = "15m"
M30 = "30m"
H1 = "1h"
H2 = "2h"
H4 = "4h"
H6 = "6h"
H8 = "8h"
H12 = "12h"
D1 = "1d"
D3 = "3d"
W1 = "1w"
MO1 = "1M"
MIN_IN_H = 60
H_IN_D = 24
D_IN_W = 7


def get_timeframe_index_from_other(
    requested_timeframe: str, provided_timeframe: str, provided_index: int
) -> int:
    req_tf_mult = get_num_of_minutes_from_timeframe(requested_timeframe)
    prov_tf_mult = get_num_of_minutes_from_timeframe(provided_timeframe)
    req_tf_index = int(provided_index * prov_tf_mult / req_tf_mult)
    return req_tf_index


def get_num_of_minutes_from_timeframe(timeframe: str) -> int:
    if "m" in timeframe:
        return int(timeframe.replace("m", ""))
    elif "h" in timeframe:
        return int(timeframe.replace("h", "")) * MIN_IN_H
    elif "d" in timeframe:
        return int(timeframe.replace("d", "")) * MIN_IN_H * H_IN_D
    elif "w" in timeframe:
        return int(timeframe.replace("w", "")) * MIN_IN_H * H_IN_D * D_IN_W
    return 0


def trades_to_dataframe(trades: List[Trade]) -> DataFrame:
    trades_df = DataFrame()
    for i, trade in enumerate(trades):
        frame = DataFrame(trade.to_dict(), index=[i + 1])
        trades_df = pd.concat([trades_df, frame])
    return trades_df
