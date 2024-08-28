"""
Module providing functions to create a Flask Application,
create a HTTP Server, and service that server via waitress.

Functions
---------
start_http_server():
    Takes a waitress- served http server, running a flask application, and
    runs it on a separate thread.

create_http_server():
    Takes a Flask Application & creates a HTTP server via waitress. The
    server is listening on port 8080.

create_flask_application(url):
    Defines and returns a Flask Application with a set of endpoints. Those
    endpoints are:

    /index:
        A sanity-check return from the root url

    /ready:
        An endpoint that will return a 202 code to signify that the benchmarks
        are ready to start
"""

import logging
import threading
from waitress.server import create_server
from flask import Flask

logger = logging.getLogger(__name__)


def start_http_server():
    app = create_flask_application()
    http_server = create_http_server(app)
    thread = threading.Thread(target=http_server.run)
    thread.start()
    logger.info("Started pgbm http server")
    return thread, http_server


def create_http_server(flask_app):
    return create_server(flask_app, listen='0.0.0.0:8080')


def create_flask_application():
    flask_app = Flask(__name__)

    @flask_app.route('/')
    def index():
        return 'At: Index'

    @flask_app.route('/ready')
    def ready():
        logger.debug("Received request to start Benchmark Instance")
        return '', 202

    return flask_app
