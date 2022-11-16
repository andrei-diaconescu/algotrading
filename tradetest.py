import unittest
import pandas as pd

from algotrading.trade import Trade

ENTRY = 100
SL = 99
TP = 101

class TestTradeMethods(unittest.TestCase):

    def test_update_trade(self):
        trade = Trade(ENTRY, "LONG", '2022-10-01 01:30:00',
                      sl_price=SL, tp_price=TP)
        self.assertEqual(trade.drawdown_price, 100)
        self.assertEqual(trade.peek_price, 100)
        self.assertEqual(trade.drawdown, 0)
        self.assertEqual(trade.peek, 0)
        self.assertEqual(trade.risk_to_reward, 1)
        self.assertEqual(trade.result, None)
        self.assertEqual(trade.peek, 0)
        self.assertEqual(trade.drawdown, 0)
        self.assertEqual(trade.price_risk, 1)

        candle = pd.DataFrame()
        candle.low = 99.8
        candle.high = 100.2
        trade.update_trade(candle)
        self.assertEqual(trade.drawdown_price, candle.low)
        self.assertEqual(trade.peek_price, candle.high)
        self.assertEqual(round(trade.drawdown, 2), 0.2)
        self.assertEqual(round(trade.peek, 2), 0.2)

        candle.low = 99.3
        candle.high = 99.7
        trade.update_trade(candle)
        self.assertEqual(trade.drawdown_price, candle.low)
        self.assertEqual(trade.peek_price, 100.2)
        self.assertEqual(round(trade.drawdown, 2), 0.7)
        self.assertEqual(round(trade.peek, 2), 0.2)

        candle.low = 99.1
        candle.high = 100.9
        trade.update_trade(candle)
        self.assertEqual(trade.drawdown_price, candle.low)
        self.assertEqual(trade.peek_price, candle.high)
        self.assertEqual(round(trade.drawdown, 2), 0.9)
        self.assertEqual(round(trade.peek, 2), 0.9)

        # trigger SL
        candle.low = 98.3
        candle.high = 99.7
        trade.update_trade(candle)
        self.assertEqual(trade.drawdown_price, 99.1)
        self.assertEqual(trade.peek_price, 100.9)
        self.assertEqual(round(trade.drawdown, 2), 0.9)
        self.assertEqual(round(trade.peek, 2), 0.9)



if __name__ == '__main__':
    unittest.main()
