"""
Module containing the main() function, that calls the fetch results function
with specified start/end times and the generate results report function
that generates the benchmarking result report.

Functions
---------
fetch_results(start_time, end_time):
    Function uses the metric classes imported from the 'metrics' module,
    to fetch results as defined in each, taking the start and end time
    args passed when called from main(). Returns results.

result_service():
    Function defines 'start_time' and 'end_time', invokes the fetch_results
    function and calls the generate_report function from the imported 'report'
    module.

Note: This Module/Script is the "main" script.
"""
import time
import logging
import sys

from pgbm.report import report
from pgbm.wait import init_wait_pgbm
from pgbm.api import http_server

from pgbm.metrics.metric import TxPerSecondMetric
from pgbm.utils.benchmark_utils import str_to_bool
from pgbm.utils.benchmark_utils import get_env_var

logger = logging.getLogger('result-service')


def fetch_results():
    results = {}

    metrics = {
        TxPerSecondMetric()
    }

    for metric in metrics:
        results[metric.name] = metric.result

    return results


def result_service(api_server):
    if init_wait_pgbm.wait_for_benchmark():
        logger.info("Benchmark job has finished, beginning to collect results")

    end_time = time.time()
    start_time = end_time - 1200
    logger.debug(f"Benchmark Start Time is - {str(start_time)}"
                 f"and End Time is  + {str(end_time)}")

    results = fetch_results()
    logger.debug(f"Results: {str(results)}")

    thresholds = report.parse_threshold_configmap()
    generated_report = report.generate_report(thresholds, results)
    logger.info(generated_report)

    agent_enabled = str_to_bool(get_env_var('AGENT_ENABLED'))
    if agent_enabled:
        report.send_report(generated_report)

    if thread.is_alive():
        logger.debug("Report has been generated & sent; closing HTTP Server")
        api_server.close()


def get_logging_level():
    valid_log_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR']

    try:
        log_level = get_env_var('LOGLEVEL').upper()
    except OSError:
        logger.info('LOGLEVEL environment variable missing, '
                    'defaulting to INFO')
        return 'INFO'

    if log_level not in valid_log_levels:
        logger.info('LOGLEVEL environment variable has invalid value, '
                    'defaulting to INFO')
        return 'INFO'

    return log_level


if __name__ == "__main__":
    logging.basicConfig(
        level=get_logging_level(),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    thread, server = http_server.start_http_server()
    try:
        sys.exit(result_service(server))
    except Exception as ex:
        logger.error(f"Unexpected Failure: {ex}")
        if thread.is_alive():
            logger.error("The result service raised an exception;"
                         "closing HTTP Server...")
            server.close()
        sys.exit(1)
