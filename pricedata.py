from typing import Type
import pandas as pd
from binance.client import Client
import config


INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h",
             "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]


class PriceData:
    def __init__(self, pair, start, end) -> None:
        self._pair = pair.upper()
        self._start = start
        self._end = end
        self.intervals_candles = {}

    def get_candles(self, interval: str) -> pd.DataFrame:
        """Requesting candles and returning them as pandas dataframe"""
        if interval in self.intervals_candles:
            return self.intervals_candles[interval]

        self._check_interval(interval)
        klines = self._request_candles_from_binance(interval)
        self.intervals_candles[interval] = self._create_and_return_candles_df(
            klines)
        return self.intervals_candles[interval]

    def _check_interval(self, interval):
        if interval.lower() not in INTERVALS:
            raise ValueError("Candle interval requested not available.")

    def _request_candles_from_binance(self, interval):
        client = Client(config.API_KEY, config.SECRET_KEY)
        return client.futures_historical_klines(
            self._pair, interval, self._start, self._end)

    def _create_and_return_candles_df(self, klines):
        candles_df = pd.DataFrame(klines)
        candles_df = candles_df.iloc[:, :6]
        candles_df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        candles_df['time'] = pd.to_datetime(candles_df['time'], unit='ms')
        candles_df.set_index('time', inplace=True)
        candles_df = candles_df.astype(float)
        return candles_df

    def get_data_for_file_name(self) -> str:
        return f"{self._pair} | {self._start} <---> {self._end}"
