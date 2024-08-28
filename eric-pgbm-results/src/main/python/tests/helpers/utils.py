"""
Module contains function that 'mocks' the http response from requests.get()
for use in unit testing the 'TestHttpClient' Class methods in the
'test_pm_http_client' module.

Function
--------
mock_response(status=200, text="CONTENT", raise_for_status=None):
    Function uses the imported 'mock' module and its 'Mock' class
    'side_effect' method, utilising this to create a Mock response
    object, with relevant variable values set as per the arg values
    passed in to the 'mock_response' function. Namely 'status' 'text'
    and 'raise_for_status', ensuring the Mock object will be returned
    with these values whenever the 'mock_response' function is called.
"""
from unittest import mock


def mock_response(
        status=200,
        text="CONTENT",
        raise_for_status=None):
    """
    Internal helper function for mocking the response
    received from requests.get()
    """
    mock_resp = mock.Mock()
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    mock_resp.status_code = status
    mock_resp.text = text
    return mock_resp
