""" Test module to test the correct parsing of config.yaml values. """
import unittest
from pgbm.utils.config_parser import parse_configmap


class TestConfigParser(unittest.TestCase):
    def test_parse_configmap_positive(self):
        clients, scale_factor, threads, time, \
          weight, filename, rate = parse_configmap("./resources"
                                                          "/config.yaml")
        self.assertEqual(clients, 50)
        self.assertEqual(scale_factor, 20)
        self.assertEqual(threads, 4)
        self.assertEqual(time, 30)
        self.assertEqual(weight, 1)
        self.assertEqual(filename, "custom-xl.sql")
        self.assertEqual(rate, "--rate=165")

    def test_parse_configmap_negative(self):
        try:
            parse_configmap("./resources/Negative_config.yaml")
        except Exception:
            pass
        else:
            self.fail('ExpectedException not raised')
