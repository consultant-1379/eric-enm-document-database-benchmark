"""
Module containing unit tests for the report.py module in pgbm
"""
import unittest
from unittest.mock import patch
import requests

import pytest

from pgbm.report import report
from tests.helpers import utils


class TestReport(unittest.TestCase):

    @pytest.fixture
    def setup_env(self, monkeypatch):  # pylint: disable=no-self-use
        monkeypatch.setenv('AGENT_HOSTNAME', 'eric-oss-cniv')
        monkeypatch.setenv('AGENT_PORT', '8080')
        monkeypatch.setenv('BENCH_NAME',
                           'eric-enm-document-database-benchmark')
        monkeypatch.setenv('BENCH_GROUP', 'postgres-verification')

    @pytest.mark.usefixtures("setup_env")
    @patch('pgbm.report.report.requests.post')
    def test_send_report_success(self, mock_post):
        # pylint: disable=no-self-use
        """
        Test for covering the success scenario of sending the report.
        Implicitly, no exception called implies a 202 return as any other
        return code would result in the exception being thrown.

        url creation & report loading tested using assert_called_with
        """
        mock_response = utils.mock_response(status=202)
        mock_post.return_value = mock_response

        expected_url = (
            "http://eric-oss-cniv:8080/result/postgres-verification"
            "/eric-enm-document-database-benchmark"
        )

        report.send_report('test_json_string')
        mock_post.assert_called_with(expected_url, json='test_json_string')

    @pytest.mark.usefixtures("setup_env")
    @patch('pgbm.report.report.requests.post')
    def test_send_report_failure(self, mock_post):
        mock_response = utils.mock_response(status=404)
        mock_post.return_value = mock_response
        retries = 2

        with self.assertRaises(requests.exceptions.RequestException):
            report.send_report('test_failed_json_string', retries=retries)

        self.assertEqual(mock_post.call_count, retries)
