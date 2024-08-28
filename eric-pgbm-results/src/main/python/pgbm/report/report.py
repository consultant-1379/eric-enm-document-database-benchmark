"""
Module containing functions to parse the config map for threshold values
and generate a benchmarking report.

Functions
---------
parse_threshold_configmap(path="/thresholds/config.yaml"):
    Function to parse threshold values from the 'config.yaml' file located
    at the specified location in 'path'.
    Function returns values for 'thesholds' or raises exceptions: 'OSError'
    exception if the file path cannot be opened. A 'YAMLError' exception if
    issue occurs parsing thresholds from yaml file.

generate_report(thresholds, results):
    Function takes args for 'thresholds' and 'results'. Generates the result
    report based on same, appending values for 'name', 'achievedResult',
    'expectedResult' and 'status' as 'PASS' or 'FAIL. Returns result report.

send_report(report):
    Function for sending the generated report to CNIV. The env vars
    for building the URL are fetched, and the URL is built. The
    report is then sent via a HTTP POST request to the URL.
"""
import logging
import time
import yaml
import requests
from pgbm.metrics.threshold import Threshold
from pgbm.utils.benchmark_utils import get_env_var

logger = logging.getLogger(__name__)


def parse_threshold_configmap(path="/thresholds/config.yaml"):
    logger.info("Parsing ConfigMap for Threshold Values...")
    try:
        logger.debug(f"Opening file at {path}")
        with open(path) as thresholds_cfg:
            config = thresholds_cfg.read()
    except OSError as os_error:
        logger.error(f"Failed to open {path}")
        raise os_error

    try:
        parsed_yaml = yaml.load(config, Loader=yaml.FullLoader)
    except yaml.YAMLError as error:
        logger.error(f"Error occurred while parsing thresholds: {error}")
        raise error
    except Exception as error:
        logger.error(f"Unexpected error while parsing thresholds: {error}")
        raise error

    requirements = parsed_yaml['requirements']
    thresholds = {}

    for req in requirements:
        minimum = requirements[req]['expectedResult'].get('minimum')
        maximum = requirements[req]['expectedResult'].get('maximum')

        thresholds[req] = (Threshold(req, requirements[req].get('description'),
                                     minimum=minimum, maximum=maximum))
        logger.debug(f"Parsed threshold: {thresholds[req]}")
    return thresholds


def generate_report(thresholds, results):
    logger.info("Generating benchmarking JSON report...")
    result_report = []
    for threshold_name, threshold in thresholds.items():
        logger.debug(f"Adding {threshold_name} results to report")
        if threshold.minimum is not None:
            status = threshold.minimum <= results[threshold.name]
        elif threshold.maximum is not None:
            status = threshold.maximum >= results[threshold.name]

        result_report.append({
            'name': threshold.name,
            'achievedResult': str(results[threshold.name]),
            'expectedResult': f"minimum: {threshold.minimum}"
            if threshold.minimum is not None else
            f"maximum: {threshold.maximum}",
            'status': 'PASS' if status else 'FAIL',
            'subRowDesc': threshold.description
        })

    return {
        'report': result_report, 'description': 'Postgres Benchmark Report'
    }


def send_report(report, wait_interval=5, retries=6):
    agent_host = get_env_var('AGENT_HOSTNAME')
    agent_port = get_env_var('AGENT_PORT')
    bench_name = get_env_var('BENCH_NAME')
    bench_group = get_env_var('BENCH_GROUP')

    url = f"http://{agent_host}:{agent_port}/result/{bench_group}/{bench_name}"
    logger.info(f"Sending report to {url}")

    while retries > 0:
        response = requests.post(url, json=report)
        if response.status_code == 202:
            logger.info('Report sent to CNIV Agent successfully')
            break
        retries -= 1
        if not retries:
            raise requests.exceptions.RequestException(
                'Error sending report',
                f'Server response: {response.status_code}'
            )
        time.sleep(wait_interval)
