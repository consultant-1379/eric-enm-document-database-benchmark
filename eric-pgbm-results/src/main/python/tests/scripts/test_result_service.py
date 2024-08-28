"""
Module containing the 'TestResultService' class, with a test method
to test end-to-end the result_service module functions.
"""
import unittest
import json
from unittest.mock import patch
from pgbm.report import report
import pytest
from scripts import result_service

with open('./resources/volume_usage.json') as vol_usage:
    VOL_USAGE_JSON = json.load(vol_usage)

with open('./resources/replication_slots.json') as replication_slots:
    REP_SLOTS_JSON = json.load(replication_slots)

with open('./resources/replication_lag.json') as replication_lag:
    REP_LAG_JSON = json.load(replication_lag)

with open('./resources/connection_count.json') as conn_count:
    CONNECTION_COUNT_JSON = json.load(conn_count)

with open('./resources/tx_per_second.json') as tx_per_sec:
    TX_PER_SECOND_JSON = json.load(tx_per_sec)

with open('./resources/cpu_throttling.json') as cpu_throttling:
    CPU_THROTTLING = json.load(cpu_throttling)

with open('./resources/cpu_usage.json') as cpu_usage:
    CPU_USAGE = json.load(cpu_usage)

with open('./resources/memory_usage.json') as mem_usage:
    MEMORY_USAGE = json.load(mem_usage)


# pylint: disable=inconsistent-return-statements


class TestResultService(unittest.TestCase):

    @pytest.fixture
    def setup_host(self, monkeypatch):  # pylint: disable=no-self-use
        monkeypatch.setenv('PM_HOSTNAME', '127.0.0.1:9090')

    @pytest.mark.usefixtures("setup_host")
    @patch("pgbm.metrics.metric.PrometheusHTTPClient.execute_instant_query")
    @patch("pgbm.metrics.metric.PrometheusHTTPClient.execute_range_query")
    def test_result_service_end_to_end(self, mock_range_query,
                                       mock_instant_query):
        expected_results = {'tx_per_second': 7000.0}

        with open('./resources/report.json') as resource_rpt:
            expected_report = json.load(resource_rpt)

        def http_client_side_effect(*args):
            # pylint: disable=too-many-return-statements
            print(args)
            if args[0] == "(pg_volume_stats_used_bytes{job='postgres'}" \
                          "/pg_volume_stats_capacity_bytes{job='postgres'})" \
                          "*100":
                return VOL_USAGE_JSON
            if args[0] == "pg_replication_slots_active{job='postgres'}":
                return REP_SLOTS_JSON
            if args[0] == "pg_replication_slots_pg_wal_lsn_diff{" \
                          "job='postgres'}":
                return REP_LAG_JSON
            if args[0] == "sum(pg_stat_activity_count{job='postgres'})":
                return CONNECTION_COUNT_JSON
            if args[0] == "last_over_time(pgb_tx_per_second[30m])":
                return TX_PER_SECOND_JSON
            if args[0] == "(rate(container_cpu_cfs_throttled_seconds_total" \
                          "{pod=~'"'postgres-0'"', " \
                          "container='postgres'}[1d]) or rate(" \
                          "container_cpu_cfs_throttled_seconds_total{pod" \
                          "=~'"'postgres-1'"', container='postgres'}[1d]))":
                return CPU_THROTTLING
            if args[0] == "(sum(rate(container_cpu_usage_seconds_total{" \
                          "pod=~'postgres-1'}[5m])) by (pod) / sum(" \
                          "container_spec_cpu_quota{pod=~'postgres-1'}" \
                          "/container_spec_cpu_period{pod=~'postgres-1'}) " \
                          "by (pod))*100 or  (sum(rate(" \
                          "container_cpu_usage_seconds_total{" \
                          "pod=~'postgres-0'}[5m])) by (pod) / sum(" \
                          "container_spec_cpu_quota{pod=~'postgres-0'}/" \
                          "container_spec_cpu_period{pod=~'postgres-0'}) " \
                          "by (pod))*100 ":
                return CPU_USAGE
            if args[0] == "(container_memory_rss{pod='"'postgres-0'"', " \
                          "container='postgres'} or container_memory_rss{" \
                          "pod='"'postgres-1'"', container='postgres'})":
                return MEMORY_USAGE

        mock_range_query.side_effect = http_client_side_effect
        mock_instant_query.side_effect = http_client_side_effect
        results = result_service.fetch_results()
        self.assertDictEqual(results, expected_results)

        thresholds = \
            report.parse_threshold_configmap('./resources/config.yaml')
        generated_report = report.generate_report(thresholds, results)
        self.assertDictEqual(expected_report, generated_report)
