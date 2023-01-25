import pandas as pd
from algotrading.trade import Trade
from algotrading.trend import Trend
import pytest
from datetime import datetime

ENTRY = 100
SL = 99
TP = 101
OPEN_TIME = datetime.strptime("2022-10-01 01:30:00", "%Y-%m-%d %H:%M:%S")
CLOSE_TIME = datetime.strptime("2022-10-01 01:50:00", "%Y-%m-%d %H:%M:%S")


@pytest.fixture(scope="module")
def trade():
    return Trade(ENTRY, Trend.LONG, OPEN_TIME, sl_price=SL, tp_price=TP)


def test_initial_trade_props(trade: Trade):
    assert trade.drawdown_price == 100
    assert trade.peek_price == 100
    assert trade.drawdown == 0
    assert trade.peek == 0
    assert trade.risk_to_reward == 1
    assert trade.result == None
    assert trade.peek == 0
    assert trade.drawdown == 0
    assert trade.price_risk == 1


@pytest.mark.parametrize(
    "candle_low, candle_high, expected_drawdown_price, expected_peek_price",
    [
        (99.8, 100, 99.8, 100),
        (99.3, 99.7, 99.3, 100),
        (99.1, 100.9, 99.1, 100.9),
        (98.3, 99.7, 99.1, 100.9),
    ],
)
def test_peek_and_drawdown_after_multiple_updates(
    trade: Trade,
    candle_low: float,
    candle_high: float,
    expected_drawdown_price: float,
    expected_peek_price: float,
):
    candle = pd.DataFrame()
    candle.low = candle_low
    candle.high = candle_high
    trade.update_trade(candle)
    assert trade.drawdown_price == expected_drawdown_price
    assert trade.peek_price == expected_peek_price


def test_trade_result(trade: Trade):
    assert trade.result == "loss"


@pytest.fixture(autouse=True)
def close_time_for_trade(trade: Trade):
    trade.set_close_time(CLOSE_TIME)


def test_to_dict_and_closed_trade(trade: Trade):
    trade_dict = trade.to_dict()
    assert trade_dict["open_time"] == OPEN_TIME
    assert trade_dict["close_time"] == CLOSE_TIME
    assert trade_dict["duration"] == 20
