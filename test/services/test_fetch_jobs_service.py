import json
from unittest.mock import patch, MagicMock
from src.services.fetch_jobs_service import fetch_jobs, APP_DATA_REGEX


class TestFetchJobsService:
    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    def test_fetch_jobs_no_response(self, mock_fetch_listings):
        mock_fetch_listings.return_value = None

        result = fetch_jobs("test-company")

        assert result is None
        mock_fetch_listings.assert_called_once_with("test-company")

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    def test_fetch_jobs_empty_response(self, mock_fetch_listings):
        mock_fetch_listings.return_value = ""

        result = fetch_jobs("test-company")

        assert result is None

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    def test_fetch_jobs_no_app_data_match(self, mock_fetch_listings):
        mock_fetch_listings.return_value = "<html><body>No app data here</body></html>"

        result = fetch_jobs("test-company")

        assert result is None

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    def test_fetch_jobs_invalid_json(self, mock_fetch_listings):
        mock_fetch_listings.return_value = 'window.__appData = {invalid json};'

        result = fetch_jobs("test-company")

        assert result is None

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    def test_fetch_jobs_missing_job_board_key(self, mock_fetch_listings):
        app_data = json.dumps({"otherData": "value"})
        mock_fetch_listings.return_value = f'window.__appData = {app_data};'

        result = fetch_jobs("test-company")

        assert result is None

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    def test_fetch_jobs_missing_job_postings_key(self, mock_fetch_listings):
        app_data = json.dumps({"jobBoard": {"otherData": "value"}})
        mock_fetch_listings.return_value = f'window.__appData = {app_data};'

        result = fetch_jobs("test-company")

        assert result is None

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    def test_fetch_jobs_null_job_board(self, mock_fetch_listings):
        app_data = json.dumps({"jobBoard": None})
        mock_fetch_listings.return_value = f'window.__appData = {app_data};'

        result = fetch_jobs("test-company")

        assert result is None

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    @patch("src.services.fetch_jobs_service.dicts_to_jobs")
    def test_fetch_jobs_success(self, mock_dicts_to_jobs, mock_fetch_listings):
        job_postings = [
            {"id": 1, "title": "Job 1"},
            {"id": 2, "title": "Job 2"}
        ]
        app_data = json.dumps({"jobBoard": {"jobPostings": job_postings}})
        mock_fetch_listings.return_value = f'window.__appData = {app_data};'

        mock_job1 = MagicMock()
        mock_job2 = MagicMock()
        mock_dicts_to_jobs.return_value = [mock_job1, mock_job2]

        result = fetch_jobs("test-company")

        assert result == [mock_job1, mock_job2]
        mock_dicts_to_jobs.assert_called_once_with(job_postings)

    @patch("src.services.fetch_jobs_service.ashby_client.fetch_listings")
    @patch("src.services.fetch_jobs_service.dicts_to_jobs")
    def test_fetch_jobs_empty_job_postings(self, mock_dicts_to_jobs, mock_fetch_listings):
        app_data = json.dumps({"jobBoard": {"jobPostings": []}})
        mock_fetch_listings.return_value = f'window.__appData = {app_data};'
        mock_dicts_to_jobs.return_value = []

        result = fetch_jobs("test-company")

        assert result == []
        mock_dicts_to_jobs.assert_called_once_with([])

    def test_app_data_regex_pattern(self):
        html = 'window.__appData = {"test": "value"};'
        match = APP_DATA_REGEX.search(html)
        assert match is not None
        assert match.group(1) == '{"test": "value"}'

        html = 'window.__appData={"test": "value"};'
        match = APP_DATA_REGEX.search(html)
        assert match is not None
        assert match.group(1) == '{"test": "value"}'

        html = '''window.__appData = {
            "test": "value",
            "nested": {"key": "value"}
        };'''
        match = APP_DATA_REGEX.search(html)
        assert match is not None

        html = 'no app data here'
        match = APP_DATA_REGEX.search(html)
        assert match is None
