from unittest.mock import MagicMock, patch
from src.services.filter_jobs_service import (
    _lower, _attr_or_key, _filter_by_company, filter_brazilian_friendly_jobs,
    _mark_brazilian_friendly, _has_brazil_in_secondary_locations,
    _global_filter, _eightsleep_filter, _supabase_filter, _deel_filter,
    REASON_GLOBAL_TITLE_OR_LOCATION, REASON_GLOBAL_SECONDARY_LOCATION,
    REASON_GLOBAL_DEFAULT, REASON_EIGHTSLEEP_MATCH, REASON_EIGHTSLEEP_DEFAULT,
    REASON_SUPABASE_MATCH, REASON_SUPABASE_DEFAULT, REASON_DEEL_MATCH,
    REASON_DEEL_DEFAULT, IS_BRAZILIAN_FRIENDLY_KEY
)


class TestFilterJobsService:
    def test_lower_with_string(self):
        assert _lower("HELLO") == "hello"
        assert _lower("  Test  ") == "test"

    def test_lower_with_none(self):
        assert _lower(None) == ""

    def test_lower_with_number(self):
        assert _lower(123) == "123"

    def test_attr_or_key_with_dict(self):
        obj = {"name": "test", "value": 123}
        assert _attr_or_key(obj, "name") == "test"
        assert _attr_or_key(obj, "value") == 123
        assert _attr_or_key(obj, "missing", "default") == "default"

    def test_attr_or_key_with_object(self):
        obj = MagicMock()
        obj.name = "test"
        obj.value = 123

        assert _attr_or_key(obj, "name") == "test"
        assert _attr_or_key(obj, "value") == 123

    def test_attr_or_key_with_object_missing_attr(self):
        obj = MagicMock()
        obj.name = "test"

        del obj.missing
        assert _attr_or_key(obj, "missing", "default") == "default"

    @patch("src.services.filter_jobs_service._global_filter")
    def test_filter_by_company_commure_athelas(self, mock_global_filter):
        mock_global_filter.return_value = True
        job = MagicMock()

        result = _filter_by_company(job, "commure-athelas")

        assert result is True
        mock_global_filter.assert_called_once_with(job)

    @patch("src.services.filter_jobs_service._global_filter")
    def test_filter_by_company_posthog(self, mock_global_filter):
        mock_global_filter.return_value = False
        job = MagicMock()

        result = _filter_by_company(job, "posthog")

        assert result is False
        mock_global_filter.assert_called_once_with(job)

    @patch("src.services.filter_jobs_service._eightsleep_filter")
    def test_filter_by_company_eightsleep(self, mock_eightsleep_filter):
        mock_eightsleep_filter.return_value = True
        job = MagicMock()

        result = _filter_by_company(job, "eightsleep")

        assert result is True
        mock_eightsleep_filter.assert_called_once_with(job)

    @patch("src.services.filter_jobs_service._supabase_filter")
    def test_filter_by_company_supabase(self, mock_supabase_filter):
        mock_supabase_filter.return_value = True
        job = MagicMock()

        result = _filter_by_company(job, "supabase")

        assert result is True
        mock_supabase_filter.assert_called_once_with(job)

    @patch("src.services.filter_jobs_service._deel_filter")
    def test_filter_by_company_deel(self, mock_deel_filter):
        mock_deel_filter.return_value = True
        job = MagicMock()

        result = _filter_by_company(job, "deel")

        assert result is True
        mock_deel_filter.assert_called_once_with(job)

    def test_filter_by_company_unknown(self):
        job = MagicMock()

        result = _filter_by_company(job, "unknown-company")

        assert result is False

    @patch("src.services.filter_jobs_service.job_to_friendly_job")
    @patch("src.services.filter_jobs_service._filter_by_company")
    def test_filter_brazilian_friendly_jobs_success(self, mock_filter_by_company, mock_job_to_friendly):
        job1 = MagicMock()
        job2 = MagicMock()
        job3 = MagicMock()
        jobs = [job1, job2, job3]

        friendly_job1 = MagicMock()
        friendly_job2 = MagicMock()
        friendly_job3 = MagicMock()

        mock_job_to_friendly.side_effect = [friendly_job1, friendly_job2, friendly_job3]
        mock_filter_by_company.side_effect = [True, False, True]

        result = filter_brazilian_friendly_jobs(jobs, "test-company")

        assert len(result) == 2
        assert friendly_job1 in result
        assert friendly_job3 in result
        assert friendly_job2 not in result

        assert mock_job_to_friendly.call_count == 3
        assert mock_filter_by_company.call_count == 3

    @patch("src.services.filter_jobs_service.job_to_friendly_job")
    @patch("src.services.filter_jobs_service._filter_by_company")
    def test_filter_brazilian_friendly_jobs_none_pass(self, mock_filter_by_company, mock_job_to_friendly):
        job1 = MagicMock()
        jobs = [job1]

        friendly_job1 = MagicMock()
        mock_job_to_friendly.return_value = friendly_job1
        mock_filter_by_company.return_value = False

        result = filter_brazilian_friendly_jobs(jobs, "test-company")

        assert len(result) == 0
        assert result == []

    @patch("src.services.filter_jobs_service.job_to_friendly_job")
    @patch("src.services.filter_jobs_service._filter_by_company")
    def test_filter_brazilian_friendly_jobs_empty_list(self, mock_filter_by_company, mock_job_to_friendly):
        jobs = []

        result = filter_brazilian_friendly_jobs(jobs, "test-company")

        assert len(result) == 0
        assert result == []
        mock_job_to_friendly.assert_not_called()
        mock_filter_by_company.assert_not_called()

    def test_mark_brazilian_friendly(self):
        job = MagicMock()
        _mark_brazilian_friendly(job, True, "test_reason")

        assert hasattr(job, 'is_brazilian_friendly')
        assert job.is_brazilian_friendly == {'isFriendly': True, 'reason': 'test_reason'}

    def test_has_brazil_in_secondary_locations_with_brazil(self):
        job = MagicMock()
        location1 = MagicMock()
        location1.locationName = "Brazil Office"
        location2 = MagicMock()
        location2.locationName = "US Office"
        job.secondaryLocations = [location1, location2]

        result = _has_brazil_in_secondary_locations(job)
        assert result is True

    def test_has_brazil_in_secondary_locations_without_brazil(self):
        job = MagicMock()
        location1 = MagicMock()
        location1.locationName = "US Office"
        location2 = MagicMock()
        location2.locationName = "UK Office"
        job.secondaryLocations = [location1, location2]

        result = _has_brazil_in_secondary_locations(job)
        assert result is False

    def test_has_brazil_in_secondary_locations_empty_list(self):
        job = MagicMock()
        job.secondaryLocations = []

        result = _has_brazil_in_secondary_locations(job)
        assert result is False

    def test_has_brazil_in_secondary_locations_none(self):
        job = MagicMock()
        job.secondaryLocations = None

        result = _has_brazil_in_secondary_locations(job)
        assert result is False

    def test_global_filter_brazil_in_title(self):
        job = MagicMock()
        job.title = "Software Engineer - Brazil"
        job.locationName = "Remote"
        job.secondaryLocations = []

        result = _global_filter(job)
        assert result is True

    def test_global_filter_brazil_in_location(self):
        job = MagicMock()
        job.title = "Software Engineer"
        job.locationName = "Brazil Remote"
        job.secondaryLocations = []

        result = _global_filter(job)
        assert result is True

    @patch('src.services.filter_jobs_service._has_brazil_in_secondary_locations')
    def test_global_filter_brazil_in_secondary_locations(self, mock_has_brazil):
        job = MagicMock()
        job.title = "Software Engineer"
        job.locationName = "Remote"
        mock_has_brazil.return_value = True

        result = _global_filter(job)
        assert result is True

    def test_global_filter_no_brazil_match(self):
        job = MagicMock()
        job.title = "Software Engineer"
        job.locationName = "Remote"
        job.secondaryLocations = []

        result = _global_filter(job)
        assert result is False

    def test_eightsleep_filter_latam_in_location(self):
        job = MagicMock()
        job.locationName = "LATAM Remote"

        result = _eightsleep_filter(job)
        assert result is True

    def test_eightsleep_filter_no_latam_match(self):
        job = MagicMock()
        job.locationName = "US Remote"

        result = _eightsleep_filter(job)
        assert result is False

    def test_supabase_filter_remote_americas_in_title(self):
        job = MagicMock()
        job.title = "Software Engineer - Americas"
        job.locationName = "Remote"

        result = _supabase_filter(job)
        assert result is True

    def test_supabase_filter_global_remote_no_parentheses(self):
        job = MagicMock()
        job.title = "Software Engineer"
        job.locationName = "Remote"

        result = _supabase_filter(job)
        assert result is True

    def test_supabase_filter_us_time_zones_in_title(self):
        job = MagicMock()
        job.title = "Engineer - US time zones"
        job.locationName = "Remote"

        result = _supabase_filter(job)
        assert result is True

    def test_supabase_filter_title_with_parentheses(self):
        job = MagicMock()
        job.title = "Engineer (Remote)"
        job.locationName = "Remote"

        result = _supabase_filter(job)
        assert result is False

    def test_supabase_filter_not_remote_location(self):
        job = MagicMock()
        job.title = "Americas Engineer"
        job.locationName = "San Francisco"

        result = _supabase_filter(job)
        assert result is True

    def test_supabase_filter_no_match(self):
        job = MagicMock()
        job.title = "Software Engineer"
        job.locationName = "US Office"

        result = _supabase_filter(job)
        assert result is False

    def test_deel_filter_anywhere_latam(self):
        job = MagicMock()
        job.locationName = "Anywhere (LATAM)"

        result = _deel_filter(job)
        assert result is True

    def test_deel_filter_anywhere_only(self):
        job = MagicMock()
        job.locationName = "Anywhere"

        result = _deel_filter(job)
        assert result is False

    def test_deel_filter_latam_only(self):
        job = MagicMock()
        job.locationName = "LATAM Office"

        result = _deel_filter(job)
        assert result is False

    def test_deel_filter_no_match(self):
        job = MagicMock()
        job.locationName = "US Remote"

        result = _deel_filter(job)
        assert result is False


class TestConstants:
    def test_constants_defined(self):
        assert IS_BRAZILIAN_FRIENDLY_KEY == 'is_brazilian_friendly'
        assert REASON_GLOBAL_TITLE_OR_LOCATION == '[global_filter] Brazil in title or location'
        assert REASON_GLOBAL_SECONDARY_LOCATION == '[global_filter] Brazil in secondary location'
        assert REASON_GLOBAL_DEFAULT == 'global_filter'
        assert REASON_EIGHTSLEEP_MATCH == '[eightsleep_filter] LATAM in location'
        assert REASON_EIGHTSLEEP_DEFAULT == 'eightsleep_filter'
        assert REASON_SUPABASE_MATCH == '[supabase_filter] Location remote and specific to americas or global'
        assert REASON_SUPABASE_DEFAULT == 'supabase_filter'
        assert REASON_DEEL_MATCH == '[deel_filter] Anywhere (LATAM) in location'
        assert REASON_DEEL_DEFAULT == 'deel_filter'
