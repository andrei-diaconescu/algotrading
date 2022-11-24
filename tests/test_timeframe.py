from algotrading.timeframe import Timeframe
import pytest


def test_get_timeframe_index_from_other() -> None:
    def assert_get_timeframe_index_from_other_with_result(
        requested_timeframe: Timeframe,
        provided_timeframe: Timeframe,
        provided_index,
        result_index,
    ):
        assert (
            provided_timeframe.from_index_to_other_timeframe_index(
                provided_index, requested_timeframe
            )
            == result_index
        )

    # LTF -> HTF
    assert_get_timeframe_index_from_other_with_result(
        Timeframe.M5, Timeframe.M1, 50, 10
    )
    assert_get_timeframe_index_from_other_with_result(Timeframe.M5, Timeframe.M1, 4, 0)
    assert_get_timeframe_index_from_other_with_result(Timeframe.M5, Timeframe.M1, 45, 9)
    assert_get_timeframe_index_from_other_with_result(
        Timeframe.M30, Timeframe.M1, 50, 1
    )
    assert_get_timeframe_index_from_other_with_result(Timeframe.H1, Timeframe.M1, 50, 0)
    assert_get_timeframe_index_from_other_with_result(Timeframe.H2, Timeframe.M1, 50, 0)
    assert_get_timeframe_index_from_other_with_result(Timeframe.W1, Timeframe.H4, 20, 0)
    #  HTF -> LTF
    assert_get_timeframe_index_from_other_with_result(Timeframe.H2, Timeframe.H4, 3, 6)
    assert_get_timeframe_index_from_other_with_result(Timeframe.M5, Timeframe.H1, 3, 36)
    assert_get_timeframe_index_from_other_with_result(Timeframe.M1, Timeframe.M3, 3, 9)
    assert_get_timeframe_index_from_other_with_result(Timeframe.D1, Timeframe.W1, 2, 14)

    def test_next_timeframe() -> None:
        assert Timeframe.M1.next_timeframe() == Timeframe.M3
        assert Timeframe.M3.next_timeframe() == Timeframe.M5
        assert Timeframe.M5.next_timeframe() == Timeframe.M15
        assert Timeframe.M15.next_timeframe() == Timeframe.M30
        assert Timeframe.M30.next_timeframe() == Timeframe.H1
        assert Timeframe.H1.next_timeframe() == Timeframe.H2
        assert Timeframe.H2.next_timeframe() == Timeframe.H4
        assert Timeframe.H4.next_timeframe() == Timeframe.H6
        assert Timeframe.H6.next_timeframe() == Timeframe.H8
        assert Timeframe.H8.next_timeframe() == Timeframe.H12
        assert Timeframe.H12.next_timeframe() == Timeframe.D1
        assert Timeframe.D1.next_timeframe() == Timeframe.D3
        assert Timeframe.D3.next_timeframe() == Timeframe.W1
        assert Timeframe.W1.next_timeframe() == Timeframe.MO1

        with pytest.raises(
            ValueError("There is no higher timeframe than Monthly candles.")
        ):
            Timeframe.MO1.next_timeframe()
