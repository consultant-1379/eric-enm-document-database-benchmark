"""
Module containing the 'TestResultProcessor' Class, with test methods to test
the 'result_processor' module functions.
"""
import json
import unittest

from pgbm.utils import result_processor

with open('./resources/range_response.json') as range_response:
    RANGE_JSON = json.load(range_response)

with open('./resources/instant_response.json') as inst_response:
    INSTANT_JSON = json.load(inst_response)

with open('./resources/instant_response_zeroes.json') as inst_response_zeros:
    INSTANT_ZEROES_JSON = json.load(inst_response_zeros)


class TestResultProcessor(unittest.TestCase):

    def test_average_result_success(self):
        self.assertEqual(result_processor.average_result(INSTANT_JSON), 5)

    def test_average_result_value_error(self):
        with self.assertRaises(ValueError):
            result_processor.average_result(INSTANT_ZEROES_JSON)

    def test_total_result_success(self):
        self.assertEqual(result_processor.total_result(INSTANT_JSON), 10)

    def test_extract_largest_result(self):
        self.assertEqual(result_processor.extract_largest_result(
            RANGE_JSON), 6)

    def test_extract_smallest_result(self):
        self.assertEqual(result_processor.extract_smallest_result(
            RANGE_JSON), 1)

    def test_extract_latest_result(self):
        self.assertEqual(result_processor.extract_latest_result(
            RANGE_JSON), 6)
