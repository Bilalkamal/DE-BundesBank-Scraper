import pytest
import requests
from app.utils import make_request_with_backoff

# Mocked response object for successful request
class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code

def test_make_request_with_backoff_success(mocker):
    # Mock the requests.get function to return a successful response
    mocker.patch('requests.get', return_value=MockResponse(200))

    # Call the function with a valid URL
    response = make_request_with_backoff("http://example.com")

    # Assert that the response is not None
    assert response is not None

def test_make_request_with_backoff_retry(mocker):
    # Mock the requests.get function to return a 429 status code
    mocker.patch('requests.get', return_value=MockResponse(429))

    # Call the function with a valid URL
    response = make_request_with_backoff("http://example.com")

    # Assert that the response is None
    assert response is None

def test_make_request_with_backoff_error(mocker):
    # Mock the requests.get function to raise an exception
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException)

    # Call the function with a valid URL
    response = make_request_with_backoff("http://example.com")

    # Assert that the response is None
    assert response is None