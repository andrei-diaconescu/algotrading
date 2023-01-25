import pytest
from algotrading.trend import Trend


@pytest.mark.parametrize(
    "trend, expected_opposite_trend",
    [
        (Trend.LONG, Trend.SHORT),
        (Trend.NONE, Trend.NONE),
        (Trend.SHORT, Trend.LONG),
    ],
)
def test_return_opposite_trend(trend: Trend, expected_opposite_trend: Trend):
    assert trend.return_opposite_trend() == expected_opposite_trend
