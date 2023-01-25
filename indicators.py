from pandas import DataFrame, Series
from algotrading.trend import Trend

# ----- Parabolic Stop & Reverse -----

RSI_EQUILIBRIUM_POINT = 50


def get_sar_trend(sar: DataFrame, last_candle: Series) -> Trend:
    if sar.iloc[-2] <= sar.iloc[-1] < last_candle.low:
        return Trend.LONG
    if sar.iloc[-2] >= sar.iloc[-1] > last_candle.high:
        return Trend.SHORT
    return Trend.NONE


def get_last_sar_trend_length(sar: DataFrame, trend: str) -> int:
    sar_trend_length = 0
    last_sar_val = sar[-1]

    for sar_val in reversed(sar):
        if trend == Trend.LONG and sar_val > last_sar_val:
            return sar_trend_length
        elif trend == Trend.SHORT and sar_val < last_sar_val:
            return sar_trend_length

        sar_trend_length += 1
        last_sar_val = sar_val

    return sar_trend_length


# ----- Stoch Relative Index Strength -----


def get_stochrsi_reversal_trend(stoch_rsi: DataFrame) -> Trend:
    previous_k, current_k = stoch_rsi.fastk.iloc[0], stoch_rsi.fastk.iloc[1]
    previous_d, current_d = stoch_rsi.fastd.iloc[0], stoch_rsi.fastd.iloc[1]

    if stochrsi_is_oversold(previous_k, current_k):
        if not stochrsi_is_rising(previous_k, previous_d) and stochrsi_is_rising(
            current_k, current_d
        ):
            return Trend.LONG
    elif stochrsi_is_overbought(previous_k, current_k):
        if stochrsi_is_rising(previous_k, previous_d) and not stochrsi_is_rising(
            current_k, current_d
        ):
            return Trend.SHORT
    return Trend.NONE


def is_first_stochrsi_reversal(fastk, fastd, reversal_trend: str) -> bool:
    for i in range(0, fastk.shape[0] - 1):
        reversal = get_stochrsi_reversal_trend(
            fastk.iloc[i : i + 2], fastd.iloc[i : i + 2]
        )
        if reversal == reversal_trend:
            return False
    return True


def stochrsi_is_rising(fastk, fastd) -> bool:
    return fastk > fastd


def stochrsi_is_oversold(*fastks) -> bool:
    for k in fastks:
        if k < 20:
            return True
    return False


def stochrsi_is_overbought(*fastks) -> bool:
    for k in fastks:
        if k > 80:
            return True
    return False


# ----- Exponential Moving Average ------


def emas_are_descending(*emas: float):
    """ "Verifies if the given EMAs are in descending order
    Used to determine bullish market structure"""
    htf_ema = emas[0] * 2
    for ema in emas:
        ltf_ema = htf_ema
        htf_ema = ema
        if ltf_ema < htf_ema:
            return False
    return True


def emas_are_ascending(*emas: float):
    """ "Verifies if the given EMAs are in ascending order
    Used to determine bearish market structure"""
    htf_ema = 0
    for ema in emas:
        ltf_ema = htf_ema
        htf_ema = ema
        if ltf_ema > htf_ema:
            return False
    return True


# ----- Candle Patterns ------


def candle_is_green(candle: Series):
    return candle.close > candle.open


def candle_is_engulfing(first_candle: Series, engufling_candle: Series):
    if candle_is_green(first_candle) == candle_is_green(engufling_candle):
        return False
    return abs(engufling_candle.close - engufling_candle.open) > abs(
        first_candle.close - first_candle.open
    )


# ----- Relative Strength Index ------


def rsi_is_at_equilibrium(rsi_value: float) -> bool:
    return abs(rsi_value - RSI_EQUILIBRIUM_POINT) < 2


def get_rsi_trend(rsi_value: float) -> Trend:
    if rsi_value < RSI_EQUILIBRIUM_POINT:
        return Trend.SHORT
    else:
        return Trend.LONG


def rsi_is_oversold(rsi_value: float) -> bool:
    return rsi_value < 30


def rsi_is_overbought(rsi_value: float) -> bool:
    return rsi_value > 70
