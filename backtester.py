import algotrading.helper as h
from algotrading.pricedata import PriceData
from algotrading.trade import Trade
from algotrading.timeframe import Timeframe
from pandas import DataFrame


class Backtester:
    def __init__(self, pair, start, end):
        self.__price_data = PriceData(pair, start, end)
        self.outcome_candles = self.get_tf_candles(Timeframe.M1)
        self.max_w_streak = 0
        self.max_l_streak = 0
        self.w_streak = 0
        self.l_streak = 0
        self.number_of_trades = 0
        self.account_size = 100
        self.trades = []

    def get_tf_candles(self, timeframe: Timeframe) -> DataFrame:
        return self.__price_data.get_candles(timeframe)

    def backtest_trade(self, trade: Trade):
        index_number = self.outcome_candles.index.get_loc(trade.open_time)
        while trade.result is None:
            trade.update_trade(self.outcome_candles.iloc[index_number])
            index_number += 1

        trade.set_close_time(self.outcome_candles.iloc[index_number - 1].name)
        self.update_streaks(trade.result)
        self.update_account_size(trade)
        self.add_trade(trade)

    def update_streaks(self, trade_result: str):
        if trade_result == "loss":
            self.update_streaks_on_lost_trade()
        elif trade_result == "profit":
            self.update_streaks_on_won_trade()
        self.number_of_trades += 1

    def update_streaks_on_lost_trade(self):
        self.max_w_streak = max(self.max_w_streak, self.w_streak)
        self.l_streak += 1
        self.w_streak = 0

    def update_streaks_on_won_trade(self):
        self.max_l_streak = max(self.max_l_streak, self.l_streak)
        self.w_streak += 1
        self.l_streak = 0

    def update_account_size(self, trade: Trade):
        if trade.result == "loss":
            self.account_size -= 0.01 * self.account_size
        else:
            self.account_size += trade.risk_to_reward * 0.01 * self.account_size

    def add_trade(self, trade):
        self.trades.append(trade)

    def trades_to_csv(self):
        csv_name = self.format_and_return_csv_name_with_prefix("ALL")
        trades_df = h.trades_to_dataframe(self.trades)
        trades_df.to_csv(csv_name)

    def won_trades_to_csv(self):
        csv_name = self.format_and_return_csv_name_with_prefix("WON")
        trades_df = h.trades_to_dataframe(self.trades)
        win_filter = trades_df["result"] == "profit"
        trades_df[win_filter].to_csv(csv_name)

    def lost_trades_to_csv(self):
        csv_name = self.format_and_return_csv_name_with_prefix("LOST")
        trades_df = h.trades_to_dataframe(self.trades)
        win_filter = trades_df["result"] == "loss"
        trades_df[win_filter].to_csv(csv_name)

    def format_and_return_csv_name_with_prefix(self, prefix: str) -> str:
        return f"{prefix} | {self.__price_data.get_data_for_file_name()}.csv"
