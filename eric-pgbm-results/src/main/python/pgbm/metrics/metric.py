"""
Module containing the metrics base classes that the 'result_service' module
uses in its 'fetch_results' function to gather the results for each one as
defined here.

Classes
-------
BaseMetric(ABC):
RangeBaseMetric(BaseMetric, ABC):
VolumeUsageMetric(RangeBaseMetric):
ReplicationSlotMetric(RangeBaseMetric):
ReplicationLagMetric(RangeBaseMetric):
ConnectionCountMetric(RangeBaseMetric):
TxPerSecondMetric(BaseMetric):
TxLatencyMetric(BaseMetric):
CPUUsageMetric(RangeBaseMetric):
CPUThrottlingMetric(RangeBaseMetric):
MemoryUsageMetric(RangeBaseMetric):
"""
from abc import abstractmethod, ABC
from functools import cached_property
from pgbm.utils import result_processor
from pgbm.client.http_client import PrometheusHTTPClient


class BaseMetric(ABC):
    def __init__(self, name, query):
        self._client = PrometheusHTTPClient()
        self._name = name
        self._query = query

    @property
    def name(self):
        return self._name

    @property
    def query(self):
        return self._query

    @abstractmethod
    def result(self):
        pass

    def __repr__(self):
        return f'Metric("{self.name}","{self.query}")'


class RangeBaseMetric(BaseMetric, ABC):
    def __init__(self, name, query, start, end, step):
        # pylint: disable=too-many-arguments
        super().__init__(name, query)
        self._start = start
        self._end = end
        self._step = step

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def step(self):
        return self._step

    def __repr__(self):
        return f'Metric("{self.name}","{self.query}","{self.start}",' \
               f'"{self.end}","{self.step}")'


class VolumeUsageMetric(RangeBaseMetric):
    _QUERY = "(pg_volume_stats_used_bytes{job='postgres'}" \
             "/pg_volume_stats_capacity_bytes{job='postgres'})*100"

    def __init__(self, start, end, step):
        super().__init__("fs_volume_usage", self._QUERY, start, end, step)

    @cached_property
    def result(self):
        response = self._client.execute_range_query(self._query, self._start,
                                                    self._end, self._step)
        return result_processor.extract_largest_result(response)


class ReplicationSlotMetric(RangeBaseMetric):
    _QUERY = "pg_replication_slots_active{job='postgres'}"

    def __init__(self, start, end, step):
        super().__init__("replication_slots_active", self._QUERY, start,
                         end, step)

    @cached_property
    def result(self):
        response = self._client.execute_range_query(self._query, self._start,
                                                    self._end, self._step)
        return result_processor.extract_smallest_result(response)


class ReplicationLagMetric(RangeBaseMetric):
    _QUERY = "pg_replication_slots_pg_wal_lsn_diff{job='postgres'}"

    def __init__(self, start, end, step):
        super().__init__("replication_lag", self._QUERY, start, end, step)

    @cached_property
    def result(self):
        response = self._client.execute_range_query(self._query, self._start,
                                                    self._end, self._step)
        return result_processor.extract_largest_result(response)


class ConnectionCountMetric(RangeBaseMetric):
    _QUERY = "sum(pg_stat_activity_count{job='postgres'})"

    def __init__(self, start, end, step):
        super().__init__("connections", self._QUERY, start, end, step)

    @cached_property
    def result(self):
        response = self._client.execute_range_query(self._query, self._start,
                                                    self._end, self._step)
        return result_processor.extract_largest_result(response)


class TxPerSecondMetric(BaseMetric):
    _QUERY = "last_over_time(pgb_tx_per_second[30m])"

    def __init__(self):
        super().__init__("tx_per_second", self._QUERY)

    @cached_property
    def result(self):
        response = self._client.execute_instant_query(self._query)
        return result_processor.total_result(response)


class TxLatencyMetric(BaseMetric):
    _QUERY = "last_over_time(pgb_transaction_latency[30m])"

    def __init__(self):
        super().__init__("tx_latency", self._QUERY)

    @cached_property
    def result(self):
        response = self._client.execute_instant_query(self._query)
        return result_processor.average_result(response)


class CPUUsageMetric(RangeBaseMetric):
    _QUERY = "(sum(rate(container_cpu_usage_seconds_total{pod=~'postgres-1'}" \
             "[5m])) by (pod) / sum(container_spec_cpu_quota{" \
             "pod=~'postgres-1'}/container_spec_cpu_period{" \
             "pod=~'postgres-1'}) by (pod))*100 or  " \
             "(sum(rate(container_cpu_usage_seconds_total{" \
             "pod=~'postgres-0'}[5m])) by (pod) / sum(" \
             "container_spec_cpu_quota{pod=~'postgres-0'}" \
             "/container_spec_cpu_period{pod=~'postgres-0'}) by (pod))*100 "

    def __init__(self, start, end, step):
        super().__init__("cpu_usage", self._QUERY, start, end, step)

    @cached_property
    def result(self):
        response = self._client.execute_range_query(self._query, self._start,
                                                    self._end, self._step)
        return result_processor.extract_largest_result(response)


class CPUThrottlingMetric(RangeBaseMetric):
    _QUERY = "(rate(container_cpu_cfs_throttled_seconds_total" \
             "{pod=~'"'postgres-0'"', container='postgres'}[1d]) " \
             "or rate(container_cpu_cfs_throttled_seconds_total{pod" \
             "=~'"'postgres-1'"', container='postgres'}[1d]))"

    def __init__(self, start, end, step):
        super().__init__("cpu_throttling", self._QUERY, start, end, step)

    @cached_property
    def result(self):
        response = self._client.execute_range_query(self._query, self._start,
                                                    self._end, self._step)
        return result_processor.extract_largest_result(response)


class MemoryUsageMetric(RangeBaseMetric):
    _QUERY = "(container_memory_rss" \
             "{pod='"'postgres-0'"', container='postgres'} " \
             "or container_memory_rss" \
             "{pod='"'postgres-1'"', container='postgres'})"

    def __init__(self, start, end, step):
        super().__init__("memory_usage", self._QUERY, start, end, step)

    @cached_property
    def result(self):
        response = self._client.execute_range_query(self._query, self._start,
                                                    self._end, self._step)
        return result_processor.extract_largest_result(response)
