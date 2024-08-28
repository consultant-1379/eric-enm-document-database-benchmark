"""
Module containing the 'TestThreshold' class, with methods to test the
'Threshold' class methods.
"""
import unittest
from pgbm.metrics.threshold import Threshold


class TestThreshold(unittest.TestCase):

    def test_min_and_max_threshold_values(self):
        # pylint: disable=unused-variable
        with self.assertRaises(ValueError):
            test_threshold = Threshold("test", "descr", minimum=4.0,
                                       maximum=2.0)

    def test_min_and_max_threshold_unset(self):
        # pylint: disable=unused-variable
        with self.assertRaises(ValueError):
            test_threshold = Threshold("test", "descr")

    def test_create_threshold(self):  # pylint: disable=no-self-use
        # pylint: disable=unused-variable
        try:
            test_threshold = Threshold("test", "descr", minimum=5.0)
        except ValueError as error:
            assert False, f"An exception was caught during the test: {error}"
