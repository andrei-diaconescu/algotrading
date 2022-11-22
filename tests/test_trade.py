import pandas as pd
from algotrading.trade import Trade

ENTRY = 100
SL = 99
TP = 101


def test_peek_and_drawdown():
    trade = Trade(ENTRY, "LONG", "2022-10-01 01:30:00", sl_price=SL, tp_price=TP)
    assert trade.drawdown_price == 100
    assert trade.peek_price == 100
    assert trade.drawdown == 0
    assert trade.peek == 0
    assert trade.risk_to_reward == 1
    assert trade.result == None
    assert trade.peek == 0
    assert trade.drawdown == 0
    assert trade.price_risk == 1

    def assert_peek_and_drawdown_prices_after_updating_trade_with_candle(
        expected_drawdown_price,
        expected_peek_price,
        expected_drawdown_percentage,
        expected_peek_percentage,
    ):
        trade.update_trade(candle)
        assert trade.drawdown_price == expected_drawdown_price
        assert trade.peek_price == expected_peek_price

    candle = pd.DataFrame()
    candle.low = 99.8
    candle.high = 100
    assert_peek_and_drawdown_prices_after_updating_trade_with_candle(99.8, 100, 0.2, 0)

    candle.low = 99.3
    candle.high = 99.7
    assert_peek_and_drawdown_prices_after_updating_trade_with_candle(99.3, 100, 0.7, 0)

    candle.low = 99.1
    candle.high = 100.9
    assert_peek_and_drawdown_prices_after_updating_trade_with_candle(
        99.1, 100.9, 0.9, 0.9
    )

    # trigger SL
    candle.low = 98.3
    candle.high = 99.7
    assert_peek_and_drawdown_prices_after_updating_trade_with_candle(
        99.1, 100.9, 0.9, 0.9
    )
