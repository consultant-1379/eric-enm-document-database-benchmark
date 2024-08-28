"""
Processors for extracting result values from Prometheus HTTP API Responses.

Functions:

    average_result(json)
    extract_largest_result(json)
    extract_smallest_result(json)
    total_result(json)
"""
import logging

logger = logging.getLogger(__name__)

__all__ = ['average_result', 'extract_largest_result',
           'extract_smallest_result', 'extract_latest_result',
           'total_result']


def average_result(json):
    """
    For a Prometheus JSON response, return the mean from
    a list of instant results
    :param json: json to process
    """
    values = _extract_instant_values(json)
    logger.debug(f"Attempting to average value set: {values}")

    if any(v == 0 for v in values):
        raise ValueError("Unexpected ZERO in result set - exiting early as "
                         "results are invalid")

    return round(float(sum(values) / len(values)), 2)


def total_result(json):
    """
    For a Prometheus JSON response, return the sum from
    a list of instant results
    :param json: json to process
    """
    values = _extract_instant_values(json)
    logger.debug(f"Attempting to total value set: {values}")
    return round(float(sum(values)), 2)


def _extract_instant_values(json):
    return [round(float(x["value"][1]), 2) for x in json["data"]["result"]]


def extract_largest_result(json):
    """
    For a prometheus JSON response, return the largest result
    from a list of range results.
    :param json: json to process
    """
    values = _extract_range_values(json)
    return max(values)


def extract_smallest_result(json):
    """
    For a prometheus JSON response, return the smallest result
    from a list of range results.
    :param json: json to process
    """
    values = _extract_range_values(json)
    return min(values)


def extract_latest_result(json):
    values = _extract_range_values(json)
    return values[-1]


def _extract_range_values(json):
    return [round(float(x[1]), 2) for y in json["data"]["result"]
            for x in y["values"]]
