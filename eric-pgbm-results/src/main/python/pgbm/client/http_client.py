"""
Module containing the 'PrometheusHTTPClient' class, a HTTP Client for fetching
data from Prometheus, and returning the response in a JSON format.

Class
-----
PrometheusHTTPClient:
    Class containing methods for querying the instant and range query APIs
    to fetch data and returns the response.

Class Methods
-------------
execute_instant_query(query):
    Executes a query against the instant query api, for point in time
    results.

execute_range_query(query, start, end, step):
    Executes a query against the range query api, for results across a time
    range.

build_query_url(query):
    Builds a prometheus API URL for use against the instant API endpoint

build_query_range_url(query, start, end, step):
    Builds a prometheus API URL for use against the range API endpoint
"""
import logging
import json
from functools import cached_property
from pgbm.utils.benchmark_utils import get_env_var
import requests

logger = logging.getLogger(__name__)


class PrometheusHTTPClient:
    QUERY_API_PATH = "api/v1/query"
    QUERY_RANGE_API_PATH = "api/v1/query_range"

    @cached_property
    def hostname(self):  # pylint: disable=no-self-use
        return get_env_var('PM_HOSTNAME')

    def execute_instant_query(self, query):
        url = self.build_query_url(query)
        logger.info(f"Fetching instant PM data from {url}")
        response = self._fetch_request(url)
        logger.info(f"Received instant query result: {response.text}")
        return json.loads(response.text)

    def execute_range_query(self, query, start, end, step):
        url = self.build_query_url(query, start, end, step)
        logger.info(f"Fetching range PM data from {url}")
        response = self._fetch_request(url)
        logger.info(f"Received range query result: {response.text}")
        return json.loads(response.text)

    def _fetch_request(self, url):  # pylint: disable=no-self-use
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as ex:
            logger.error(f"Connection Error: Could not establish connection "
                         f"to Prometheus via URL: {url} ")
            raise ex
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            logger.error(f"HTTP Error: For URL {url} - Exception: {ex}")
            raise ex
        return response

    def build_query_url(self, query, start=None, end=None, step=None):
        if start is not None:
            return (
                f'http://{self.hostname}/{self.QUERY_RANGE_API_PATH}?'
                f'query={query}&start={start}&end={end}&step={step}'
            )

        return f'http://{self.hostname}/{self.QUERY_API_PATH}?query={query}'
