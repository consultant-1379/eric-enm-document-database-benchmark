"""
Test Module for the Benchmark Utils module
"""
import unittest
from pgbm.utils.benchmark_utils import str_to_bool


class TestBenchmarkUtils(unittest.TestCase):

    def test_str_to_bool_truthy(self):
        self.assertEqual(str_to_bool('True'), True)
        self.assertEqual(str_to_bool('true'), True)
        self.assertEqual(str_to_bool('T'), True)
        self.assertEqual(str_to_bool('t'), True)

    def test_str_to_bool_falsey(self):
        self.assertEqual(str_to_bool('False'), False)
        self.assertEqual(str_to_bool('false'), False)
        self.assertEqual(str_to_bool('F'), False)
        self.assertEqual(str_to_bool('f'), False)

    def test_str_to_bool_other_strings(self):
        self.assertEqual(str_to_bool(''), False)
        self.assertEqual(str_to_bool('1 2 3 4'), False)
        self.assertEqual(str_to_bool('abcd[][]'), False)
