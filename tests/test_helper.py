from algotrading import helper


def test_get_timeframe_index_from_other() -> None:
    def assert_get_timeframe_index_from_other_with_result(
        requested_timeframe, provided_timeframe, index, result_index
    ):
        assert (
            helper.get_timeframe_index_from_other(
                requested_timeframe, provided_timeframe, index
            )
            == result_index
        )

    # LTF -> HTF
    assert_get_timeframe_index_from_other_with_result(helper.M5, helper.M1, 50, 10)
    assert_get_timeframe_index_from_other_with_result(helper.M5, helper.M1, 4, 0)
    assert_get_timeframe_index_from_other_with_result(helper.M5, helper.M1, 45, 9)
    assert_get_timeframe_index_from_other_with_result(helper.M30, helper.M1, 50, 1)
    assert_get_timeframe_index_from_other_with_result(helper.H1, helper.M1, 50, 0)
    assert_get_timeframe_index_from_other_with_result(helper.H2, helper.M1, 50, 0)
    assert_get_timeframe_index_from_other_with_result(helper.W1, helper.H4, 20, 0)
    #  HTF -> LTF
    assert_get_timeframe_index_from_other_with_result(helper.H2, helper.H4, 3, 6)
    assert_get_timeframe_index_from_other_with_result(helper.M5, helper.H1, 3, 36)
    assert_get_timeframe_index_from_other_with_result(helper.M1, helper.M3, 3, 9)
    assert_get_timeframe_index_from_other_with_result(helper.D1, helper.W1, 2, 14)
