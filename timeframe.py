from __future__ import annotations
from enum import Enum

MIN_IN_H = 60
H_IN_D = 24
D_IN_W = 7


class Timeframe(Enum):
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

    def to_number_of_minutes(self) -> int:
        value = self.value
        if "m" in value:
            return int(value.replace("m", ""))
        elif "h" in value:
            return int(value.replace("h", "")) * MIN_IN_H
        elif "d" in value:
            return int(value.replace("d", "")) * MIN_IN_H * H_IN_D
        elif "w" in value:
            return int(value.replace("w", "")) * MIN_IN_H * H_IN_D * D_IN_W
        return 0

    def from_index_to_other_timeframe_index(
        self, provided_index: int, requested_timeframe: Timeframe
    ) -> int:
        provided_tf_multiplier = self.to_number_of_minutes()
        requested_tf_multiplier = requested_timeframe.to_number_of_minutes()
        requested_index = int(
            provided_index * provided_tf_multiplier / requested_tf_multiplier
        )
        return requested_index

    def next_timeframe(self) -> Timeframe:
        if self is Timeframe.MO1:
            raise ValueError("There is no higher timeframe than Monthly candles.")
        found = False
        for timeframe in Timeframe:
            if found:
                return timeframe
            if self is timeframe:
                found = True
