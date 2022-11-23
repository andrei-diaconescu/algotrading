from enum import Enum


class Trend(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NONE = None

    def return_opposite_trend(self):
        if self == Trend.LONG:
            return Trend.SHORT
        elif self == Trend.SHORT:
            return Trend.LONG
        return Trend.NONE
