"""
Module containing functions that provide a wait mechanism for
benchmarking to complete before exiting.

Functions
---------
get_namespace():
    Function opens and reads the file at the location specified in
    the 'NAMESPACE_PATH' variable, then sets the 'namespace' variable value
    accordingly.
    Function raises a 'FileNotFoundError' exception if file cannot be read.

get_token():
    Function opens and reads the file at the location specified in
    the 'TOKEN_PATH' variable, then sets the 'token' variable value
    accordingly.
    Function raises a 'FileNotFoundError' exception if file cannot be read.

get_job_status(url):
    Function uses the 'requests' module from the 'Requests' HTTP library
    to check the benchmarking job status by sending a http request to the
    API server at the value of the 'url' arg passed to the function.
    Function returns the content of the http response.
    Funtion will raise an 'HTTPError' exception if job 'url' provided as arg
    is incorrect or does not exist.

wait_for_benchmark():
    Function invokes the 'get_job_status' function, passing it the benchmark
    job url. It parses the job 'status' in json from the response, checking
    and intermittently sleeping until the status field 'type' is 'Complete',
    before returning 'True'.
    Function raises the following exceptions: HTTPError, ConnectionError,
    FileNotFoundError in relation to any issues.
"""
import json
import time
import logging
import requests

from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from pgbm.exceptions import PgBenchmarkError
from pgbm.utils.benchmark_utils import get_env_var

logger = logging.getLogger(__name__)

API_SERVER = "https://kubernetes.default.svc"
NAMESPACE_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
CA_CRT_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"


def get_namespace():
    try:
        with open(NAMESPACE_PATH) as namespace_path:
            namespace = namespace_path.read()
    except FileNotFoundError as ex:
        logger.error("Namespace filepath not found, cannot start container")
        raise ex

    return namespace


def get_token():
    try:
        with open(TOKEN_PATH) as token_path:
            token = token_path.read()
    except FileNotFoundError as ex:
        logger.error("Token filepath not found, cannot start container")
        raise ex

    return token


def get_job_status(url):
    try:
        token = get_token()
    except FileNotFoundError as ex:
        raise ex

    try:
        response = requests.get(url, verify=CA_CRT_PATH,
                                headers={"Authorization": f"Bearer {token}"})
    except requests.exceptions.ConnectionError as ex:
        logger.error(f"Connection Error - API Server is unavailable at {url}. "
                     f"Error: {ex}")
        raise ex
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as ex:
        logger.error(f"HTTP Error - Job does not exist or incorrect "
                     f"endpoint provided for url - {url}. Error: {ex}")
        raise ex

    return response.text


def wait_for_benchmark():
    url = f"{API_SERVER}/apis/batch/v1/namespaces/" \
          f"{get_namespace()}/jobs/{get_env_var('BENCHMARK_JOB_NAME')}"

    while True:
        try:
            job_status = get_job_status(url)
        except (HTTPError, ConnectionError, FileNotFoundError):
            logger.error("Error when fetching Job Status from the K8s API,"
                         "trying again...")
            time.sleep(5)
            continue

        job_status_json = json.loads(job_status)
        status = job_status_json["status"]

        if "conditions" not in status:
            logger.info('Benchmark Status is not "Complete", waiting...')
            time.sleep(5)
            continue

        status_dict = status["conditions"][0]

        if status_dict is not None:
            if status_dict["type"] == "Complete" and \
                    status_dict["status"] == "True":
                logger.info('Benchmark Status is "Complete"')
                return True
            if status_dict["type"] == "Failed" and \
                    status_dict["status"] == "True":
                logger.error('Benchmark Status is "Failed"')
                raise PgBenchmarkError('Status of load-tester job is '
                                       '"Failed" due to an error, check the '
                                       'load-tester logs')

        logger.info('Benchmark Status is not "Complete", waiting...')
