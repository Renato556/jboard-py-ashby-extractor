import pytest
from unittest.mock import patch, MagicMock
from src.services.jobs_service import _save_to_db, get_jobs


class TestJobsService:
    def test_save_to_db_success(self):
        mock_job1 = MagicMock()
        mock_job1.to_dict.return_value = {"title": "Job 1", "company": "Company A"}

        mock_job2 = MagicMock()
        mock_job2.to_dict.return_value = {"title": "Job 2", "company": "Company B"}

        jobs = [mock_job1, mock_job2]

        with patch("src.services.jobs_service.insert_job") as mock_insert:
            _save_to_db(jobs)

            assert mock_insert.call_count == 2
            mock_insert.assert_any_call({"title": "Job 1", "company": "Company A"})
            mock_insert.assert_any_call({"title": "Job 2", "company": "Company B"})

    @patch("src.services.jobs_service.fetch_jobs")
    def test_get_jobs_no_listings(self, mock_fetch):
        mock_fetch.return_value = None

        get_jobs("test-company")

        mock_fetch.assert_called_once_with("test-company")

    @patch("src.services.jobs_service.fetch_jobs")
    def test_get_jobs_empty_listings(self, mock_fetch):
        mock_fetch.return_value = []

        get_jobs("test-company")

        mock_fetch.assert_called_once_with("test-company")

    @patch("src.services.jobs_service.fetch_jobs")
    @patch("src.services.jobs_service.filter_brazilian_friendly_jobs")
    def test_get_jobs_no_brazilian_jobs(self, mock_filter, mock_fetch):
        mock_fetch.return_value = [MagicMock()]
        mock_filter.return_value = []

        get_jobs("test-company")

        mock_fetch.assert_called_once_with("test-company")
        mock_filter.assert_called_once()

    @patch("src.services.jobs_service.fetch_jobs")
    @patch("src.services.jobs_service.filter_brazilian_friendly_jobs")
    def test_get_jobs_no_brazilian_jobs_none(self, mock_filter, mock_fetch):
        mock_fetch.return_value = [MagicMock()]
        mock_filter.return_value = None

        get_jobs("test-company")

        mock_fetch.assert_called_once_with("test-company")
        mock_filter.assert_called_once()

    @patch("src.services.jobs_service.fetch_jobs")
    @patch("src.services.jobs_service.filter_brazilian_friendly_jobs")
    @patch("src.services.jobs_service.normalize_jobs")
    def test_get_jobs_no_normalized_jobs(self, mock_normalize, mock_filter, mock_fetch):
        mock_fetch.return_value = [MagicMock()]
        mock_filter.return_value = [MagicMock()]
        mock_normalize.return_value = []

        get_jobs("test-company")

        mock_fetch.assert_called_once_with("test-company")
        mock_filter.assert_called_once()
        mock_normalize.assert_called_once()

    @patch("src.services.jobs_service.fetch_jobs")
    @patch("src.services.jobs_service.filter_brazilian_friendly_jobs")
    @patch("src.services.jobs_service.normalize_jobs")
    def test_get_jobs_no_normalized_jobs_none(self, mock_normalize, mock_filter, mock_fetch):
        mock_fetch.return_value = [MagicMock()]
        mock_filter.return_value = [MagicMock()]
        mock_normalize.return_value = None

        get_jobs("test-company")

        mock_fetch.assert_called_once_with("test-company")
        mock_filter.assert_called_once()
        mock_normalize.assert_called_once()

    @patch("src.services.jobs_service.fetch_jobs")
    @patch("src.services.jobs_service.filter_brazilian_friendly_jobs")
    @patch("src.services.jobs_service.normalize_jobs")
    @patch("src.services.jobs_service._save_to_db")
    def test_get_jobs_success(self, mock_save, mock_normalize, mock_filter, mock_fetch):
        mock_fetch.return_value = [MagicMock()]
        mock_filter.return_value = [MagicMock()]
        mock_normalize.return_value = [MagicMock()]

        get_jobs("test-company")

        mock_fetch.assert_called_once_with("test-company")
        mock_filter.assert_called_once()
        mock_normalize.assert_called_once()
        mock_save.assert_called_once()

    @patch("src.services.jobs_service.fetch_jobs")
    @patch("src.services.jobs_service.filter_brazilian_friendly_jobs")
    @patch("src.services.jobs_service.normalize_jobs")
    @patch("src.services.jobs_service._save_to_db")
    def test_get_jobs_save_error(self, mock_save, mock_normalize, mock_filter, mock_fetch):
        mock_fetch.return_value = [MagicMock()]
        mock_filter.return_value = [MagicMock()]
        mock_normalize.return_value = [MagicMock()]
        mock_save.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            get_jobs("test-company")
