import pandas as pd
from binance.client import Client
import config
from algotrading.timeframe import Timeframe


class PriceData:
    def __init__(self, pair: str, start: str, end: str) -> None:
        self._pair = pair.upper()
        self._start = start
        self._end = end
        self.intervals_candles = {}

    def get_candles(self, timeframe: Timeframe) -> pd.DataFrame:
        """Requesting candles and returning them as pandas dataframe"""
        if timeframe in self.intervals_candles:
            return self.intervals_candles[timeframe]

        self._check_interval(timeframe)
        klines = self._request_candles_from_binance(timeframe)
        self.intervals_candles[timeframe] = self._create_and_return_candles_df(klines)
        return self.intervals_candles[timeframe]

    def _check_interval(self, timeframe: Timeframe):
        if timeframe not in Timeframe:
            raise ValueError("Candle timeframe requested not available.")

    def _request_candles_from_binance(self, timeframe: Timeframe):
        client = Client(config.API_KEY, config.SECRET_KEY)
        return client.futures_historical_klines(
            self._pair, timeframe.value, self._start, self._end
        )

    def _create_and_return_candles_df(self, klines):
        candles_df = pd.DataFrame(klines)
        candles_df = candles_df.iloc[:, :6]
        candles_df.columns = ["time", "open", "high", "low", "close", "volume"]
        candles_df["time"] = pd.to_datetime(candles_df["time"], unit="ms")
        candles_df.set_index("time", inplace=True)
        candles_df = candles_df.astype(float)
        return candles_df

    def get_data_for_file_name(self) -> str:
        return f"{self._pair} | {self._start} <---> {self._end}"
