import pytest
import os
import responses
from unittest.mock import patch, MagicMock
from requests.exceptions import Timeout, ConnectionError, RequestException
from src.clients.database_client import DatabaseClient, insert_job, health_check, _client


class TestDatabaseClient:
    @patch.dict(os.environ, {"API_URL": "https://test-api.com", "API_TIMEOUT": "45"})
    def test_init_with_custom_timeout(self):
        client = DatabaseClient()
        assert client.api_url == "https://test-api.com"
        assert client.timeout == 45

    @patch.dict(os.environ, {"API_URL": "https://test-api.com"})
    def test_init_with_default_timeout(self):
        client = DatabaseClient()
        assert client.api_url == "https://test-api.com"
        assert client.timeout == 30

    @patch.dict(os.environ, {"API_URL": "https://test-api.com"})
    def test_create_session(self):
        client = DatabaseClient()
        session = client._create_session()

        assert session.headers['Content-Type'] == 'application/json'
        assert session.headers['User-Agent'] == 'ashby-job-extractor/1.0'

    @responses.activate
    @patch.dict(os.environ, {"API_URL": "https://test-api.com"})
    def test_make_request_success(self):
        responses.add(responses.POST, "https://test-api.com/test", json={"status": "ok"}, status=200)

        client = DatabaseClient()
        response = client._make_request("POST", "test", {"data": "test"})

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    @patch.dict(os.environ, {"API_URL": "https://test-api.com"})
    def test_make_request_timeout(self):
        client = DatabaseClient()

        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = Timeout("Request timeout")

            with pytest.raises(Exception, match="API timeout after 30 seconds"):
                client._make_request("POST", "test")

    @patch.dict(os.environ, {"API_URL": "https://test-api.com"})
    def test_make_request_connection_error(self):
        client = DatabaseClient()

        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = ConnectionError("Connection failed")

            with pytest.raises(Exception, match="Failed to connect to API - check network connectivity"):
                client._make_request("POST", "test")

    @patch.dict(os.environ, {"API_URL": "https://test-api.com"})
    def test_make_request_general_exception(self):
        client = DatabaseClient()

        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = RequestException("General error")

            with pytest.raises(Exception, match="Request failed: General error"):
                client._make_request("POST", "test")

    @responses.activate
    @patch.dict(os.environ, {"API_URL": "https://test-api.com"})
    def test_make_request_endpoint_with_leading_slash(self):
        responses.add(responses.GET, "https://test-api.com/test", json={"status": "ok"}, status=200)

        client = DatabaseClient()
        response = client._make_request("GET", "/test")

        assert response.status_code == 200


class TestInsertJob:
    @patch("src.clients.database_client._client")
    def test_insert_job_success_201(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_client._make_request.return_value = mock_response

        job = {"title": "Test Job", "company": "Test Company"}
        insert_job(job)

        mock_client._make_request.assert_called_once_with('POST', 'jobs', job)

    @patch("src.clients.database_client._client")
    def test_insert_job_already_exists_304(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 304
        mock_client._make_request.return_value = mock_response

        job = {"title": "Test Job", "company": "Test Company"}
        insert_job(job)

        mock_client._make_request.assert_called_once_with('POST', 'jobs', job)

    @patch("src.clients.database_client._client")
    def test_insert_job_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.ok = False
        mock_response.text = "Internal Server Error"
        mock_client._make_request.return_value = mock_response

        job = {"title": "Test Job", "company": "Test Company"}

        with pytest.raises(Exception, match="Error inserting job: 500"):
            insert_job(job)

    @patch("src.clients.database_client._client")
    def test_insert_job_without_title(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_client._make_request.return_value = mock_response

        job = {"company": "Test Company"}
        insert_job(job)

        mock_client._make_request.assert_called_once_with('POST', 'jobs', job)


class TestHealthCheck:
    @patch("src.clients.database_client._client")
    def test_health_check_success(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client._make_request.return_value = mock_response

        result = health_check()

        assert result is True
        mock_client._make_request.assert_called_once_with('GET', 'health')

    @patch("src.clients.database_client._client")
    def test_health_check_failure(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client._make_request.return_value = mock_response

        result = health_check()

        assert result is False

    @patch("src.clients.database_client._client")
    def test_health_check_exception(self, mock_client):
        mock_client._make_request.side_effect = Exception("Connection failed")

        result = health_check()

        assert result is False
