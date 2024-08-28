"""
Module containing functions for running benchmarking and exporting metrics.
Imports the 'pgbench' and 'collect_metrics' modules to facilitate the above.

Functions
---------
run_benchmark():
    Function uses the imported 'pgbench' module, invoking its 'PgBench' class
    methods to run benchmarking as defined in that class.

export_metrics():
    Function uses the imported 'collect_metrics' module, invoking its
    'MetricExporter' class methods to gather benchmark metric values
    ('tps' and 'latency') and setting these in prometheus.

main():
    Function invokes the 'run_benchmark' and 'export_metrics' functions of
    this module.
"""
import sys
import logging
from pgbm.metrics.collect_metrics import MetricExporter
from pgbm.pgbench.pgbench import PgBench

logger = logging.getLogger('benchmark-service')


def run_benchmark():
    pgbench = PgBench()
    pgbench.check_database_exists()
    pgbench.create_database()
    pgbench.initialise_database()
    pgbench.run_pgbench()


def export_metrics():
    metrics_exporter = MetricExporter()
    tps, latency, lag = metrics_exporter.get_values("/pgbench/output.txt")
    metrics_exporter.set_metrics(tps, latency, lag)


def main():
    run_benchmark()
    export_metrics()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - '
                                                   '%(levelname)s - %('
                                                   'message)s')
    try:
        sys.exit(main())
    except Exception as ex:
        logger.error(f"Unexpected Failure: {ex}")
        sys.exit(1)
