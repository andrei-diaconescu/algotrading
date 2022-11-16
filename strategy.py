from algotrading.backtester import Backtester


class Strategy:
    def __init__(self, **kwargs) -> None:
        pass

    def backtest_pair_and_period(self, timeframe: str, pair: str, start: str, end: str):
        self.initialize_backtester(pair, start, end)
        self.prepare_backtesting_data(timeframe)
        self.backtest()

    def initialize_backtester(self, pair, start, end):
        self.backtester = Backtester(pair, start, end)

    def prepare_backtesting_data(self, timeframe):
        self.main_timeframe = timeframe
        self.bt_main_candles = self.backtester.get_tf_candles(
            self.main_timeframe)

    def backtest(self):
        pass

    def conditions_are_met(self, **kwargs) -> bool:
        pass

    def trade(self, **kwargs):
        pass

    def calc_entry(self, **kwargs) -> float:
        pass

    def calc_take_profit(self, **kwargs) -> float:
        pass

    def calc_stop_loss(self, **kwargs) -> float:
        pass

    def conditions_are_met(self, **kwargs) -> bool:
        pass