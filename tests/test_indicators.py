import pytest
import algotrading.indicators as i
from algotrading.trend import Trend
import pandas as pd

# ----- Stoch Relative Index Strength -----


@pytest.mark.parametrize(
    "fastk, fastd, expected",
    [
        (12, 13, False),
        (13, 13, False),
        (27, 13, True),
    ],
)
def test_stochrsi_is_rising(fastk, fastd, expected):
    assert i.stochrsi_is_rising(fastk, fastd) == expected


@pytest.mark.parametrize(
    "stochrsi_val,expected",
    [
        (0, True),
        (19.9999, True),
        (20, False),
        (53, False),
    ],
)
def test_single_stochrsi_is_oversold(stochrsi_val, expected):
    assert i.stochrsi_is_oversold(stochrsi_val) == expected


@pytest.mark.parametrize(
    "stochrsi_values,expected",
    [
        ([20, 50], False),
        ([14, 20], False),
        ([13.7, 17.34], True),
    ],
)
def test_multiple_stochrsi_is_oversold(stochrsi_values, expected):
    assert i.stochrsi_is_oversold(*stochrsi_values) == expected


@pytest.mark.parametrize(
    "stochrsi_val,expected",
    [
        (0, False),
        (79.9999999, False),
        (80, False),
        (93, True),
    ],
)
def test_single_stochrsi_is_overbought(stochrsi_val, expected):
    assert i.stochrsi_is_overbought(stochrsi_val) == expected


@pytest.mark.parametrize(
    "stochrsi_values,expected",
    [
        ([30, 80], False),
        ([80, 81], False),
        ([83, 97], True),
    ],
)
def test_multiple_stochrsi_is_overbought(stochrsi_values, expected):
    assert i.stochrsi_is_overbought(*stochrsi_values) == expected


# ----- Exponential Moving Average ------


@pytest.fixture
def descending_emas():
    return [100, 70, 40]


@pytest.fixture
def ascending_emas():
    return [40, 70, 100]


@pytest.fixture
def mixed_order_emas():
    return [100, 40, 70]


@pytest.mark.parametrize(
    "emas, expected",
    [
        ("descending_emas", False),
        ("ascending_emas", True),
        ("mixed_order_emas", False),
    ],
)
def test_emas_are_ascending(emas, expected, request):
    emas = request.getfixturevalue(emas)
    assert i.emas_are_ascending(*emas) == expected


@pytest.mark.parametrize(
    "emas, expected",
    [
        ("descending_emas", True),
        ("ascending_emas", False),
        ("mixed_order_emas", False),
    ],
)
def test_emas_are_descending(emas, expected, request):
    emas = request.getfixturevalue(emas)
    assert i.emas_are_descending(*emas) == expected


# ----- Candle Patterns ------
@pytest.fixture
def basic_candle_indexes():
    return ["open", "close"]


@pytest.fixture
def green_candle(basic_candle_indexes):
    return pd.Series([100, 101], index=basic_candle_indexes)


@pytest.fixture
def small_red_candle(basic_candle_indexes):
    return pd.Series([101, 100.5], index=basic_candle_indexes)


@pytest.fixture
def big_red_candle(basic_candle_indexes):
    return pd.Series([101, 99], index=basic_candle_indexes)


@pytest.mark.parametrize(
    "first_candle, second_candle, expected",
    [
        ("green_candle", "big_red_candle", True),
        ("green_candle", "small_red_candle", False),
        ("small_red_candle", "green_candle", True),
        ("small_red_candle", "big_red_candle", False),
        ("big_red_candle", "green_candle", False),
    ],
)
def test_candle_is_engulfing(first_candle, second_candle, expected, request):
    first_candle = request.getfixturevalue(first_candle)
    second_candle = request.getfixturevalue(second_candle)
    assert i.candle_is_engulfing(first_candle, second_candle) == expected


# ----- Relative Strength Index ------


@pytest.mark.parametrize(
    "rsi_value, expected",
    [
        (24, False),
        (47.9999, False),
        (48, False),
        (50, True),
        (51.9999, True),
        (52, False),
        (52.0000, False),
        (86, False),
    ],
)
def test_rsi_is_at_equilibrium(rsi_value, expected):
    assert i.rsi_is_at_equilibrium(rsi_value) == expected


@pytest.mark.parametrize(
    "rsi_value, expected_trend",
    [
        (24, Trend.SHORT),
        (47.9999, Trend.SHORT),
        (50, Trend.LONG),
        (51.9999, Trend.LONG),
        (52, Trend.LONG),
        (52.0000, Trend.LONG),
        (86, Trend.LONG),
    ],
)
def test_get_rsi_trend(rsi_value, expected_trend):
    assert i.get_rsi_trend(rsi_value) == expected_trend


@pytest.mark.parametrize(
    "rsi_value, expected",
    [
        (50, False),
        (30, False),
        (29.99, True),
        (17, True),
    ],
)
def test_rsi_is_oversold(rsi_value, expected):
    assert i.rsi_is_oversold(rsi_value) == expected


@pytest.mark.parametrize(
    "rsi_value, expected",
    [
        (50, False),
        (30, False),
        (70, False),
        (70.00001, True),
        (83, True),
    ],
)
def test_rsi_is_overbought(rsi_value, expected):
    assert i.rsi_is_overbought(rsi_value) == expected
