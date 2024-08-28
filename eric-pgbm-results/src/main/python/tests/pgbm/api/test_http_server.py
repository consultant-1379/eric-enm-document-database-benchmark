"""Test Module for the HTTP Server functionality"""
# pylint: disable=redefined-outer-name
import pytest
import waitress.server

from pgbm.api.http_server import create_flask_application, create_http_server


@pytest.fixture()
def app():
    app = create_flask_application()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_request_index(client):
    response = client.get("/")
    assert response.text == "At: Index"


def test_request_ready(client):
    response = client.get("/ready")
    assert response.status == "202 ACCEPTED"


def test_create_http_server(app):
    server = create_http_server(app)
    assert isinstance(server, waitress.server.TcpWSGIServer)
