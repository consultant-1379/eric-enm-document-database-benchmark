""" Test module provides unit tests for init_wait_pgbm functions. """
import json
import unittest

from unittest.mock import patch, mock_open

import pytest
import requests
from requests import HTTPError

from pgbm.wait import init_wait_pgbm
from pgbm.exceptions import PgBenchmarkError
from tests.helpers import utils


with open('./resources/kube_api_job_status_success.json') as api_job_success:
    SUCCESS_JSON = json.load(api_job_success)

with open('./resources/kube_api_job_status_failed.json') as api_job_failed:
    FAILED_JSON = json.load(api_job_failed)


class TestInitWaitPGBM(unittest.TestCase):

    @pytest.fixture
    def setup_env(self, monkeypatch):  # pylint: disable=no-self-use
        monkeypatch.setenv('BENCHMARK_JOB_NAME',
                           'eric-enm-document-database-benchmark-load-tester')

    @pytest.mark.usefixtures("setup_env")
    @patch('pgbm.wait.init_wait_pgbm.requests.get')
    @patch('pgbm.wait.init_wait_pgbm.get_token')
    @patch('pgbm.wait.init_wait_pgbm.get_namespace')
    def test_init_wait_pgbm(self, mock_get_namespace,
                            mock_get_token, mock_get):
        mock_get_namespace.return_value = "test_namespace"
        mock_get_token.return_value = "test_token"
        mock_get.return_value = utils.mock_response(
            text=json.dumps(SUCCESS_JSON))

        self.assertTrue(init_wait_pgbm.wait_for_benchmark())

    @pytest.mark.usefixtures("setup_env")
    @patch('pgbm.wait.init_wait_pgbm.requests.get')
    @patch('pgbm.wait.init_wait_pgbm.get_token')
    @patch('pgbm.wait.init_wait_pgbm.get_namespace')
    def test_job_status_failed(self, mock_get_namespace,
                               mock_get_token, mock_get):
        mock_get_namespace.return_value = "test_namespace"
        mock_get_token.return_value = "test_token"
        mock_get.return_value = utils.mock_response(
            text=json.dumps(FAILED_JSON))

        with self.assertRaises(PgBenchmarkError):
            init_wait_pgbm.wait_for_benchmark()

    @patch('pgbm.wait.init_wait_pgbm.get_token')
    def test_job_status_token_exception(self, mock_get_token):
        mock_get_token.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            init_wait_pgbm.get_job_status("url")

    @patch('pgbm.wait.init_wait_pgbm.get_token')
    def test_job_status_connection_error(
            self, mock_get_token):
        mock_get_token.return_value = "test_token"
        with self.assertRaises(requests.exceptions.ConnectionError):
            init_wait_pgbm.get_job_status("http://127.0.0.1/fail")

    @patch('pgbm.wait.init_wait_pgbm.get_token')
    @patch('pgbm.wait.init_wait_pgbm.requests.get')
    def test_job_status_http_error(
            self, mock_get, mock_get_token):
        mock_get_token.return_value = "test_token"
        mock_response = utils.mock_response(
            status=404, raise_for_status=HTTPError("Non 200 status code"))
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPError):
            init_wait_pgbm.get_job_status("http://127.0.0.1/fail")

    @patch('builtins.open', new_callable=mock_open, read_data="test_token")
    def test_get_token(self, mock_file):  # pylint: disable=unused-argument
        self.assertEqual(init_wait_pgbm.get_token(), "test_token")

    @patch('builtins.open', new_callable=mock_open, read_data="test_namespace")
    def test_get_namespace(self, mock_file):  # pylint: disable=unused-argument
        self.assertEqual(init_wait_pgbm.get_namespace(), "test_namespace")

    @patch('builtins.open', new_callable=mock_open)
    def test_get_token_file_exception(self, mock_file):
        mock_file.side_effect = FileNotFoundError()
        with self.assertRaises(FileNotFoundError):
            init_wait_pgbm.get_token()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_namespace_file_exception(self, mock_file):
        mock_file.side_effect = FileNotFoundError()
        with self.assertRaises(FileNotFoundError):
            init_wait_pgbm.get_namespace()
