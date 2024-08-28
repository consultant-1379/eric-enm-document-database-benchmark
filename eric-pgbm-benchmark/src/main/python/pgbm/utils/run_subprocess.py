"""
Module containing function that spawns a new process to run a command with the
args passed to the function and returns the output code.

Function
--------
execute_command(password, user, client, database, query):
    Function invokes a subprocess using the run() function to run a
    command with the args 'password', 'user', 'client', 'database'.
    Once the command completes this function returns the value of the
    return code from the command or will raise a relevant exception
    specifying the error generated.
"""
import re
import subprocess
import logging

logger = logging.getLogger(__name__)

PG_AUTH_FAIL_REGEX = r"FATAL\s*:\s+password\s+authentication\s+failed"
PG_DB_EXISTS_REGEX = r"ERROR\s*:\s+database\s+.\w+.\s+already\s+exists"
PG_BENCH_NOT_EXIST_REGEX = r"pgbench\s*:\s+command\s+not\s+found"
PSQL_NOT_EXIST_REGEX = r"psql\s*:\s+command\s+not\s+found"


def execute_command(password, user, client, database, query):
    try:
        execute = subprocess.run(f"PGPASSWORD={str(password)} {str(client)} "
                                 f"-U {str(user)} -h postgres "
                                 f"{str(query)} {database} ;", shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError as error:
        if re.search(PG_AUTH_FAIL_REGEX, str(error.stdout)):
            logger.error(f"Authentication error: {str(error)} \n "
                         f"{str(error.stdout)}")
            raise error
        if re.search(PG_BENCH_NOT_EXIST_REGEX, str(error.stdout)):
            logger.error(f"Postgres binary does not exist: {str(error)} \n "
                         f"{str(error.stdout)}")
            raise error
        if re.search(PG_DB_EXISTS_REGEX, str(error.stdout)):
            logger.error(f"DB already exists: {str(error)} \n "
                         f"{str(error.stdout)}")
            raise error
        if re.search(PSQL_NOT_EXIST_REGEX, str(error.stdout)):
            logger.error(f"Postgres binary does not exist: {str(error)} \n "
                         f"{str(error.stdout)}")
            raise error

        logger.error(f"Command Failed: {str(error)} \n {str(error.stdout)}")
        raise error
    return execute
