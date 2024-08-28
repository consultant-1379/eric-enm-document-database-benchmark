"""
Utilities for use across pgbm

Functions:

    str_to_bool(string):
        Converts a string representation of a boolean
        value into a Boolean.

    get_env_var(var_name):
        Fetches an environment variable with the
        given name from the os. Throws an OSError
        if the given env var doesn't exist.
"""
import logging
import os

logger = logging.getLogger(__name__)


def str_to_bool(string):
    if string in ("True", "true", "T", "t"):
        return True

    return False


def get_env_var(var_name):
    try:
        env_var = os.getenv(var_name)
        if env_var is None:
            raise OSError
    except OSError as ex:
        logger.error(f"Environment Variable {var_name} not set")
        raise ex
    return env_var
