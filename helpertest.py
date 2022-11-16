import unittest

import helper


class TestHelperMethods(unittest.TestCase):

    def test_get_timeframe_index_from_other(self):
        provided_timeframe = helper.M1
        provided_index = 50
        requested_timeframe = helper.M5
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 10)

        provided_timeframe = helper.M1
        provided_index = 4
        requested_timeframe = helper.M5
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 0)

        provided_timeframe = helper.M1
        provided_index = 45
        requested_timeframe = helper.M5
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 9)

        provided_timeframe = helper.M1
        provided_index = 50
        requested_timeframe = helper.M30
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 1)

        provided_timeframe = helper.M1
        provided_index = 50
        requested_timeframe = helper.H1
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 0)

        provided_timeframe = helper.M1
        provided_index = 50
        requested_timeframe = helper.H2
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 0)

        provided_timeframe = helper.H4
        provided_index = 3
        requested_timeframe = helper.H2
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 6)

        provided_timeframe = helper.H4
        provided_index = 20
        requested_timeframe = helper.W1
        requested_index = helper.get_timeframe_index_from_other(
            requested_timeframe, provided_timeframe, provided_index)
        self.assertEqual(requested_index, 0)


if __name__ == '__main__':
    unittest.main()
