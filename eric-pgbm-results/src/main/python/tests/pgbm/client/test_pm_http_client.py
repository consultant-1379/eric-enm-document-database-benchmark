"""
Module contains the 'TestHttpClient' class with methods that test the
'PrometheusHTTPClient' class methods for API requests/responses in the
'http_client' module.
"""
import json
import unittest
from unittest.mock import patch
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
import pytest
from pgbm.client.http_client import PrometheusHTTPClient
from tests.helpers import utils

with open('./resources/range_response.json') as range_response:
    RANGE_JSON = json.load(range_response)

with open('./resources/instant_response.json') as inst_response:
    INSTANT_JSON = json.load(inst_response)


class TestHttpClient(unittest.TestCase):
    @pytest.fixture
    def setup_host(self, monkeypatch):  # pylint: disable=no-self-use
        monkeypatch.setenv('PM_HOSTNAME', '127.0.0.1:9090')

    @pytest.fixture
    def setup_incorrect_host(self, monkeypatch):  # pylint: disable=no-self-use
        monkeypatch.setenv('PM_HOSTNAME', 'incorrect')

    @pytest.mark.usefixtures("setup_host")
    def test_build_query_url(self):
        pm_client = PrometheusHTTPClient()
        self.assertEqual(pm_client.build_query_url("up{job='postgres'}"),
                         "http://127.0.0.1:9090/api/v1/query?query=up{"
                         "job='postgres'}")

    @pytest.mark.usefixtures("setup_host")
    def test_build_query_range_url(self):
        pm_client = PrometheusHTTPClient()
        self.assertEqual(pm_client.build_query_url("up{job='postgres'}",
                                                   "2022-09-07T15:30:00.781Z",
                                                   "2022-09-07T16:20:00.781Z",
                                                   "10s"),
                         "http://127.0.0.1:9090/api/v1/query_range?query=up{"
                         "job=""'postgres'}&start=2022-09-07T15:30:00.781Z"
                         "&end=2022-09-07T16:20:00.781Z&step=10s")

    @pytest.mark.usefixtures("setup_incorrect_host")
    def test_fetch_request_connection_error(self):
        pm_client = PrometheusHTTPClient()
        with self.assertRaises(ConnectionError):
            pm_client.execute_instant_query("test_query")

    def test_missing_hostname(self):
        pm_client = PrometheusHTTPClient()
        with self.assertRaises(OSError):
            pm_client.execute_instant_query("test_query")

    @pytest.mark.usefixtures("setup_host")
    @patch('pgbm.client.http_client.requests.get')
    def test_fetch_request_success(self, mock_get):
        pm_client = PrometheusHTTPClient()
        mock_resp = utils.mock_response(text=json.dumps(INSTANT_JSON))
        mock_get.return_value = mock_resp

        self.assertEqual(pm_client.execute_instant_query("test_query"),
                         INSTANT_JSON)

    @pytest.mark.usefixtures("setup_host")
    @patch('pgbm.client.http_client.requests.get')
    def test_fetch_range_request_success(self, mock_get):
        pm_client = PrometheusHTTPClient()
        mock_resp = utils.mock_response(text=json.dumps(RANGE_JSON))
        mock_get.return_value = mock_resp

        self.assertEqual(
            pm_client.execute_range_query(
                "test_query", "start", "end", "step"), RANGE_JSON)

    @pytest.mark.usefixtures("setup_host")
    @patch('pgbm.client.http_client.requests.get')
    def test_fetch_request_http_error(self, mock_get):
        pm_client = PrometheusHTTPClient()
        mock_resp = utils.mock_response(status=404, raise_for_status=HTTPError(
            "Non 200 status code"))
        mock_get.return_value = mock_resp

        with self.assertRaises(HTTPError):
            pm_client.execute_instant_query("test_query")
