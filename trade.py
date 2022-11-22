from pandas import DataFrame


class Trade:
    def __init__(
        self, entry_price: float, side: str, open_time, position_size=float(1), **kwargs
    ) -> None:
        self.open_time = open_time
        self.close_time = kwargs.get("close_time", None)
        self.trade_duration = kwargs.get("trade_duration", 0)
        self.set_entry_price(entry_price)
        sl_price = kwargs.get("sl_price", None)
        if sl_price is not None:
            self.set_stop_loss(sl_price)
        tp_price = kwargs.get("tp_price", None)
        if tp_price is not None:
            self.set_take_profit_price(tp_price)
        self.update_rr()
        self.set_price_risk()
        self.set_side(side)
        self.set_position_size(position_size)
        self.result = kwargs.get("result", None)
        self.peek_price = self.entry
        self.drawdown_price = self.entry
        self.peek = 0
        self.drawdown = 0

    def set_entry_price(self, entry_price: float):
        self.check_price_value(entry_price)
        self.entry = entry_price

    def set_stop_loss(self, sl_price: float):
        self.check_price_value(sl_price)
        self.stop_loss = round(sl_price, 2)
        self.sl_percentage = abs(self.entry - self.stop_loss) * 100 / self.entry

    def set_take_profit_price(self, tp_price: float):
        self.check_price_value(tp_price)
        self.take_profit = round(tp_price, 2)
        self.tp_percentage = abs(self.entry - self.take_profit) * 100 / self.entry

    def set_price_risk(self):
        self.price_risk = abs(self.take_profit - self.entry) / self.risk_to_reward

    def set_position_size(self, position_size: float):
        if position_size <= 0:
            raise ValueError("Position size must be greater than 0.")
        self.position_size = position_size

    def set_side(self, side: str):
        side = side.upper()
        if side != "LONG" and side != "SHORT":
            raise ValueError(
                f'Position type value must be either "LONG" or "SHORT". Actual value: {side}'
            )
        self.side = side

    def check_price_value(self, price: float):
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

    def update_rr(self):
        if self.take_profit == None or self.stop_loss == None:
            self.risk_to_reward = 0
        else:
            rr = self.tp_percentage / self.sl_percentage
            self.risk_to_reward = round(rr, 2)

    def calc_current_risk(self, price: float):
        price_dif = price - self.entry
        return price_dif / self.price_risk

    def set_close_time(self, close_time):
        self.close_time = close_time
        self.trade_duration = (self.close_time - self.open_time).total_seconds() / 60

    def to_dict(self) -> dict:
        trade_dict = {
            "open_time": self.open_time,
            "close_time": self.close_time,
            "duration": self.trade_duration,
            "side": self.side,
            "entry": self.entry,
            "stop_loss": self.stop_loss,
            "sl_perc": self.sl_percentage,
            "take_profit": self.take_profit,
            "tp_perc": self.tp_percentage,
            "risk_to_reward": self.risk_to_reward,
            "drawdown": self.drawdown,
            "peek": self.peek,
            "result": self.result,
        }
        return trade_dict

    def update_trade(self, candle):
        if self.result is None:
            if self.side == "LONG":
                self.update_long_result(candle)
            else:
                self.update_short_result(candle)

            if self.result is None:
                self.update_drawdown_price(candle)
                self.update_peek_price(candle)
            else:
                if self.result == "profit":
                    self.drawdown = -(abs(self.calc_current_risk(self.drawdown_price)))
                    self.peek = self.risk_to_reward
                else:
                    self.drawdown = -1 / self.risk_to_reward
                    self.peek = abs(self.calc_current_risk(self.peek_price))

    def update_short_result(self, candle):
        if candle.low <= self.take_profit:
            self.result = "profit"
        elif candle.high >= self.stop_loss:
            self.result = "loss"

    def update_long_result(self, candle):
        if candle.high >= self.take_profit:
            self.result = "profit"
        elif candle.low <= self.stop_loss:
            self.result = "loss"

    def update_drawdown_price(self, candle):
        if self.side == "LONG":
            self.drawdown_price = min(candle.low, self.drawdown_price)
        else:
            self.drawdown_price = max(candle.high, self.drawdown_price)

    def update_peek_price(self, candle):
        if self.side == "LONG":
            self.peek_price = max(candle.high, self.peek_price)
        else:
            self.peek_price = min(candle.low, self.drawdown_price)
