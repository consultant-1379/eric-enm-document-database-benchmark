"""
Test module provides testing of functions gathering positive/negative metric
values and tests the metrics port used to export values.
"""
import unittest
import pytest
from pgbm.metrics.collect_metrics import MetricExporter


class TestCollectMetrics(unittest.TestCase):

    @pytest.fixture
    def setup_port(self, monkeypatch):  # pylint: disable=no-self-use
        monkeypatch.setenv('METRICS_PORT', '9600')

    def test_get_values_positive_with_rate(self):
        exporter = MetricExporter()
        tx_per_sec, latency_avg, lag = \
            exporter.get_values("./resources/MockPGbenchOutputWithRate.txt")
        self.assertEqual(tx_per_sec.group(0), "tps = 5381.265150 (including "
                                              "connections establishing)")
        self.assertEqual(latency_avg.group(0), "latency average = 9.291 ms")
        self.assertEqual(lag.group(0), "lag: avg 11.320")

    def test_get_values_positive_without_rate(self):
        exporter = MetricExporter()
        tx_per_sec, latency_avg, lag = \
            exporter.get_values("./resources/MockPGbenchOutputWithoutRate.txt")
        self.assertEqual(tx_per_sec.group(0), "tps = 5381.265150 (including "
                                              "connections establishing)")
        self.assertEqual(latency_avg.group(0), "latency average = 9.291 ms")
        self.assertEqual(lag, None)

    def test_get_values_negative(self):
        exporter = MetricExporter()
        tx_per_sec, latency_avg, lag = \
            exporter.get_values("./resources/NegativePGBenchLookup.txt")
        self.assertEqual(tx_per_sec, None)
        self.assertEqual(latency_avg, None)
        self.assertEqual(lag, None)

    @pytest.mark.usefixtures("setup_port")
    def test_get_metrics_port(self):
        exporter = MetricExporter()
        self.assertEqual('9600', exporter.get_metrics_port())
