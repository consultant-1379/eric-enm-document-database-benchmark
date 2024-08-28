"""
Module containing the 'MetricExporter' class with methods for the
collection and export of metrics to prometheus.

Class
-----
MetricExporter:
    Class to collect and export metrics to prometheus over HTTP.

Class Methods
-------------
    get_metrics_port(self):
        Method extracts the value of the environment variable 'METRICS_PORT'
        if present. Otherwise, raises 'OSError' exception.

    http_server_start(self):
        Method starts up the http server to expose the metrics via specifed
        metrics port passed in as parameter arg when method is called.

    get_values(self, path):
        Method uses a regular expression search for 'tps' and 'latency' values
        in the file located at the specifed 'path' arg passed to the method.
        Returns those values.

    set_metrics(self, tps, latency):
        Method sets the metrics in prometheus, specifically, the 'tps' and
        transaction 'latency' args passed to this method.
"""
import os
from time import sleep
import re
import logging
from prometheus_client import start_http_server, Gauge

logger = logging.getLogger(__name__)


class MetricExporter:

    def get_metrics_port(self):
        # pylint: disable=no-self-use
        try:
            metrics_port = os.getenv('METRICS_PORT')
            if metrics_port is None:
                raise OSError
        except OSError as error:
            logger.error("Metrics Port not present or "
                         "misconfigured. Exiting...")
            raise error
        return metrics_port

    def http_server_start(self):
        metrics_port = self.get_metrics_port()
        start_http_server(int(metrics_port))

    def get_values(self, path):
        # pylint: disable=no-self-use
        tps = re.compile(r'tps = (\d+.\d+) [(](including) \w+ \w+[)]')
        latency = re.compile(r"latency average = (\d+.\d+) \w+")
        lag_avg = re.compile(r"lag: avg (\d+.\d+)")

        try:
            file = open(path, 'r')
        except OSError as error:
            logger.error(f"Could not open/read file: {path}")
            raise error

        with file:
            lines = file.readlines()
            for line in lines:
                tps_i = tps.search(line)
                lat = latency.search(line)
                lag = lag_avg.search(line)

        return tps_i, lat, lag

    def set_metrics(self, tps, latency, lag):
        self.http_server_start()
        tps_metric = Gauge("pgb_tx_per_second",
                           "Transactions per second including the"
                           " time taken in order to establish connections")
        latency_metric = Gauge("pgb_transaction_latency",
                               "Average elapsed transaction"
                               " time of each statement")
        i = 0
        if tps and latency is not None:
            lag_avg = 0
            if lag is not None:
                lag_avg = float(lag.group(1))
                logger.info(f"lag average: {lag_avg}")
            latency_avg = float(latency.group(1)) - lag_avg
            logger.info("Setting metrics in prometheus")
            logger.info(f"Setting tps value of {str(float(tps.group(1)))}")
            logger.info(f"Setting transaction latency value of "
                        f"{str(latency_avg)}")
            while i < 15:
                tps_metric.set(float(tps.group(1)))
                latency_metric.set(latency_avg)
                i = i + 1
                sleep(5)
        else:
            logger.error(f"Metrics not found. "
                         f"Returned: {str(tps)} and {str(latency)}")
