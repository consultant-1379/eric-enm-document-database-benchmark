"""
Module containing the 'PgBench' class with methods for the creation and
initialisation of a database and the running of benchmarks against same.

Class
-----
PgBench:
    Class for creating/initialising a database and running of benchmarking
    against the same.

Class Methods
-------------
    check_database_exists(self):
        Method executes command running psql query that checks if 'mydb'
        database exists in the 'pg_database' table.

    create_database(self):
        Method runs the 'createdb' command to create the 'mydb'
        + 5 character random ID string database when called.

    initialise_database(self):
        Method runs command to initialise the database 'mydb'
        + 5 character random ID string when called.

    run_pgbench(self):
        Method runs 'Insert/Select/Update/Delete' statements for configured
        time duration against the specified database for
        benchmarking purposes.
"""
import logging
from pgbm.utils.run_subprocess import execute_command
from pgbm.utils.config_parser import parse_secret, parse_configmap
from pgbm.utils.generate_database_name import id_generator

logger = logging.getLogger(__name__)


class PgBench:
    def __init__(self, mydb='mydb'):
        self.mydb = mydb
        self.clients, self.scale_factor, \
          self.threads, self.time, self.weight, \
            self.filename, self.rate = parse_configmap()
        self.password, self.user = parse_secret()
        self.path = '/pgbench/output.txt'

    def check_database_exists(self):
        self.mydb = self.mydb + id_generator()
        while True:
            check_db_exists = execute_command(self.password, self.user, "psql",
                                              "", "-c \" select exists("
                                                  "select datname from "
                                                  "pg_database "
                                                  "where datname = "
                                                  f"'{str(self.mydb)}')\"")
            if str(check_db_exists.stdout).__contains__(' t'):
                self.mydb = 'mydb' + id_generator()
            elif str(check_db_exists.stdout).__contains__(' f'):
                break

    def create_database(self):
        execute_command(self.password, self.user, "createdb", self.mydb, "")
        logger.info(f"Creating database {self.mydb}")

    def initialise_database(self):
        execute_command(self.password, self.user, "pgbench", self.mydb,
                        f"-i -s {str(self.scale_factor)}")
        logger.info(f"Initialising database {self.mydb}")

    def run_pgbench(self):
        try:
            file = open(self.path, 'a+')
        except OSError as error:
            logger.error(f"Could not open file: {self.path}")
            raise error
        with file:
            run = execute_command(self.password, self.user, "pgbench",
                  self.mydb, f"-f /var/tmp/"
                             f"{self.filename} "
                             f"-c {self.clients} "
                             f"-j {self.threads} -n "
                             f" -b simple-update@"
                             f"{self.weight} -T "
                             f"{self.time} "
                             f"{self.rate if self.rate is not None else ' '}")
            logger.info(f"Running Delete, Insert, Select and Update"
                        " statements against database"
                        f" {self.mydb} for {self.time} seconds")
            try:
                file.write(str(run.stdout))
            except OSError as error:
                logger.error("Error writing to file:  ", exc_info=True)
                raise error
