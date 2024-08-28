"""
Test module containing tests of the 'id_genertor' function
in the 'generate_database_name' module
"""
import unittest
from pgbm.utils.generate_database_name import id_generator


class TestGenerateDatabaseName(unittest.TestCase):
    def test_id_generator_returns_random(self):
        self.assertNotEqual(id_generator(), id_generator())

    def test_id_string_length(self):
        a_str = "aaaaa"
        b_str = id_generator()
        self.assertEqual(a_str.__len__(), b_str.__len__())
