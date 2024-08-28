"""
Module containing functions that parse user and password values along with
config values from the respective files associated with each.

Functions
---------
parse_secret():
    Function parses password and user values from files located at
    specified filepaths and returns those values. Raises 'OSError'
    exception if files cannot be read.

parse_configmap(path="/config/config.yaml"):
    Function parses config values for 'clients/scale_factor/threads/time'
    from the 'config.yaml' file located at the specified filepath.
    Function returns values for same or raises 'OSError' exception
    if file cannot be read.
"""
import logging
import yaml

logger = logging.getLogger(__name__)


def parse_secret():
    try:
        with open("/secret/super-pwd") as secret_pw:
            password = secret_pw.read()
        with open("/secret/super-user") as secret_user:
            user = secret_user.read()
    except OSError as error:
        logger.error("Could not read from secret")
        raise error
    return password, user


def parse_configmap(path="/config/config.yaml"):
    try:
        with open(path) as config_cfg:
            config = config_cfg.read()
    except OSError as error:
        logger.error(f"Could not open/read file: {path}")
        raise error
    try:
        parsed_yaml = yaml.load(config, Loader=yaml.FullLoader)
        clients = parsed_yaml['pgbench']['clients']
        scale_factor = parsed_yaml["pgbench"]['scale_factor']
        threads = parsed_yaml['pgbench']['threads']
        time = parsed_yaml['pgbench']['time']
        weight = parsed_yaml['pgbench']['weight']
        filename = parsed_yaml['pgbench']['filename']
        rate = parsed_yaml['pgbench']['rate']
        if clients is None:
            logger.error("Error with config.yaml file, "
                         f"pgbench value is None\n clients:{clients}, "
                         "not set correctly")
            raise Exception
        if scale_factor is None:
            logger.error("Error with config.yaml file, "
                         "pgbench value is None\n scale_factor:"
                         f"{scale_factor} not set correctly")
            raise Exception
        if threads is None:
            logger.error("Error with config.yaml file, "
                         f"pgbench value is None\n threads:{threads} "
                         "not set correctly")
            raise Exception
        if time is None:
            logger.error("Error with config.yaml file, "
                         f"pgbench value is None\n time:{time} "
                         "not set correctly")
            raise Exception
        if weight is None:
            logger.error("Error with config.yaml file, "
                         f"pgbench value is None\n weight:{weight} "
                         "not set correctly")
            raise Exception
        if filename is None:
            logger.error("Error with config.yaml file, "
                         f"pgbench value is None\n filename:{filename} "
                         "not set correctly")
            raise Exception
    except yaml.YAMLError as error:
        logger.error(f"Error parsing the config.yaml file: {path}")
        raise error

    return clients, scale_factor, threads, time, weight, filename, rate
