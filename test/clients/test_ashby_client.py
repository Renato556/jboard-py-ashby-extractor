import os
import responses
from unittest.mock import patch
from requests.exceptions import RequestException, Timeout, ConnectionError
from src.clients.ashby_client import fetch_listings


class TestAshbyClient:
    @responses.activate
    @patch.dict(os.environ, {
        "DEFAULT_URL": "https://jobs.ashbyhq.com/",
        "ASHBY_TIMEOUT": "30.0"
    })
    def test_fetch_listings_success(self):
        responses.add(
            responses.GET,
            "https://jobs.ashbyhq.com/test-company",
            body="<html>job listings content</html>",
            status=200
        )
        
        result = fetch_listings("test-company")
        
        assert result == "<html>job listings content</html>"

    @responses.activate
    @patch.dict(os.environ, {
        "DEFAULT_URL": "https://jobs.ashbyhq.com/",
        "ASHBY_TIMEOUT": "30.0"
    })
    def test_fetch_listings_http_error(self):
        responses.add(
            responses.GET,
            "https://jobs.ashbyhq.com/test-company",
            status=404
        )
        
        result = fetch_listings("test-company")
        
        assert result is None

    @patch.dict(os.environ, {
        "DEFAULT_URL": "https://jobs.ashbyhq.com/",
        "ASHBY_TIMEOUT": "30.0"
    })
    @patch("requests.get")
    def test_fetch_listings_request_exception(self, mock_get):
        mock_get.side_effect = RequestException("Network error")
        
        result = fetch_listings("test-company")
        
        assert result is None

    @patch.dict(os.environ, {
        "DEFAULT_URL": "https://jobs.ashbyhq.com/",
        "ASHBY_TIMEOUT": "30.0"
    })
    @patch("requests.get")
    def test_fetch_listings_timeout_exception(self, mock_get):
        mock_get.side_effect = Timeout("Request timeout")
        
        result = fetch_listings("test-company")
        
        assert result is None

    @patch.dict(os.environ, {
        "DEFAULT_URL": "https://jobs.ashbyhq.com/",
        "ASHBY_TIMEOUT": "30.0"
    })
    @patch("requests.get")
    def test_fetch_listings_connection_error(self, mock_get):
        mock_get.side_effect = ConnectionError("Connection failed")
        
        result = fetch_listings("test-company")
        
        assert result is None

    @patch.dict(os.environ, {
        "DEFAULT_URL": "https://jobs.ashbyhq.com/",
        "ASHBY_TIMEOUT": "30.0"
    })
    @patch("requests.get")
    def test_fetch_listings_unexpected_exception(self, mock_get):
        mock_get.side_effect = ValueError("Unexpected error")
        
        result = fetch_listings("test-company")
        
        assert result is None

    @responses.activate
    @patch.dict(os.environ, {
        "DEFAULT_URL": "https://jobs.ashbyhq.com/",
        "ASHBY_TIMEOUT": "15.5"
    })
    def test_fetch_listings_custom_timeout(self):
        responses.add(
            responses.GET,
            "https://jobs.ashbyhq.com/custom-company",
            body="content",
            status=200
        )
        
        result = fetch_listings("custom-company")

        assert result == "content"
