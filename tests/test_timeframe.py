from algotrading.timeframe import Timeframe
import pytest


def test_list() -> None:
    expected = [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    ]
    assert Timeframe.list() == expected


def test_primary_timeframes_property() -> None:
    expected = [
        "15m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
    ]
    assert Timeframe.primary_timeframes() == expected


@pytest.mark.parametrize(
    "provided_timeframe, provided_index, requested_timeframe, expected_index",
    [
        #  LTF - HTF
        (Timeframe.M1, 50, Timeframe.M5, 10),
        (Timeframe.M1, 4, Timeframe.M5, 0),
        (Timeframe.M1, 45, Timeframe.M5, 9),
        (Timeframe.M1, 50, Timeframe.M30, 1),
        (Timeframe.M1, 50, Timeframe.H1, 0),
        (Timeframe.M1, 50, Timeframe.H2, 0),
        (Timeframe.H4, 20, Timeframe.W1, 0),
        #  HTF -> LTF
        (Timeframe.H4, 3, Timeframe.H2, 6),
        (Timeframe.H1, 3, Timeframe.M5, 36),
        (Timeframe.M3, 3, Timeframe.M1, 9),
        (Timeframe.W1, 2, Timeframe.D1, 14),
    ],
)
def test_get_timeframe_index_from_other(
    provided_timeframe: Timeframe,
    provided_index: int,
    requested_timeframe: Timeframe,
    expected_index: int,
) -> None:
    assert (
        provided_timeframe.from_index_to_other_timeframe_index(
            provided_index, requested_timeframe
        )
        == expected_index
    )


@pytest.mark.parametrize(
    "first_timeframe,next_timeframe",
    [
        (Timeframe.M1, Timeframe.M3),
        (Timeframe.M3, Timeframe.M5),
        (Timeframe.M5, Timeframe.M15),
        (Timeframe.M15, Timeframe.M30),
        (Timeframe.M30, Timeframe.H1),
        (Timeframe.H1, Timeframe.H2),
        (Timeframe.H2, Timeframe.H4),
        (Timeframe.H4, Timeframe.H6),
        (Timeframe.H6, Timeframe.H8),
        (Timeframe.H8, Timeframe.H12),
        (Timeframe.H12, Timeframe.D1),
        (Timeframe.D1, Timeframe.D3),
        (Timeframe.D3, Timeframe.W1),
        (Timeframe.W1, Timeframe.MO1),
    ],
)
def test_next_timeframe(first_timeframe: Timeframe, next_timeframe: Timeframe) -> None:
    assert first_timeframe.next_timeframe() == next_timeframe


def test_next_timeframe_month():
    with pytest.raises(ValueError):
        Timeframe.MO1.next_timeframe()
