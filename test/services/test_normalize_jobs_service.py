import pytest
import os
from unittest.mock import patch, MagicMock
from src.services.normalize_jobs_service import (
    _define_url, _set_seniority, _normalize_seniority, _set_field,
    _normalize_field, normalize_jobs
)
from src.models.enums.seniority_enum import SeniorityEnum
from src.models.enums.field_enum import FieldEnum


class TestNormalizeJobsService:
    @patch.dict(os.environ, {"DEFAULT_URL": "https://jobs.ashbyhq.com/"})
    def test_define_url_normal_company(self):
        url = _define_url("test-company", "job-123")
        assert url == "https://jobs.ashbyhq.com/test-company/job-123"

    @patch.dict(os.environ, {"DEFAULT_URL": "https://jobs.ashbyhq.com/"})
    def test_define_url_company_with_space(self):
        url = _define_url("test company", "job-123")
        assert url == "https://jobs.ashbyhq.com/test%20company/job-123"

    def test_set_seniority(self):
        job = MagicMock()
        _set_seniority(job, SeniorityEnum.SENIOR)
        assert job.seniority_level == SeniorityEnum.SENIOR.value

    def test_normalize_seniority_staff_keywords(self):
        test_cases = [
            "Staff Engineer",
            "Engineering Director",
            "Head of Engineering",
            "Engineering Manager",
            "Lead Developer"
        ]

        for title in test_cases:
            job = MagicMock()
            job.title = title
            _normalize_seniority(job)
            assert job.seniority_level == SeniorityEnum.STAFF.value

    def test_normalize_seniority_senior_keywords(self):
        test_cases = [
            "Senior Software Engineer",
            "Sr. Developer",
            "Tech Lead Engineer",
            "Software Architect",
            "Expert Developer"
        ]

        for title in test_cases:
            job = MagicMock()
            job.title = title
            _normalize_seniority(job)
            assert job.seniority_level == SeniorityEnum.SENIOR.value

    def test_normalize_seniority_junior_keywords(self):
        test_cases = [
            "Junior Developer",
            "Entry_Level Engineer",
            "Associate Software Engineer"
        ]

        for title in test_cases:
            job = MagicMock()
            job.title = title
            _normalize_seniority(job)
            assert job.seniority_level == SeniorityEnum.JUNIOR.value

    def test_normalize_seniority_intern(self):
        job = MagicMock()
        job.title = "Software Engineering Intern"
        _normalize_seniority(job)
        assert job.seniority_level == SeniorityEnum.INTERN.value

    def test_normalize_seniority_mid_level_default(self):
        job = MagicMock()
        job.title = "Software Engineer"
        _normalize_seniority(job)
        assert job.seniority_level == SeniorityEnum.MID_LEVEL.value

    def test_normalize_seniority_manager_with_senior(self):
        job = MagicMock()
        job.title = "Senior Engineering Manager"
        _normalize_seniority(job)
        assert job.seniority_level == SeniorityEnum.SENIOR.value

    def test_normalize_seniority_tech_lead(self):
        job = MagicMock()
        job.title = "Tech Lead Engineer"
        _normalize_seniority(job)
        assert job.seniority_level == SeniorityEnum.SENIOR.value

    def test_normalize_seniority_team_lead(self):
        job = MagicMock()
        job.title = "Team Lead Developer"
        _normalize_seniority(job)
        assert job.seniority_level == SeniorityEnum.SENIOR.value

    def test_normalize_seniority_empty_title(self):
        job = MagicMock()
        job.title = ""
        _normalize_seniority(job)
        assert job.seniority_level == SeniorityEnum.MID_LEVEL.value

    def test_normalize_seniority_no_title_attr(self):
        job = MagicMock()
        del job.title
        _normalize_seniority(job)
        assert job.seniority_level == SeniorityEnum.MID_LEVEL.value

    def test_set_field(self):
        job = MagicMock()
        _set_field(job, FieldEnum.ENGINEERING.value)
        assert job.field == FieldEnum.ENGINEERING.value

    def test_normalize_field_data(self):
        test_cases = [
            {"departmentName": "Data", "title": "Engineer"},
            {"departmentName": "S&M", "title": "Engineer"},
            {"departmentName": "Engineering", "title": "Data Scientist"}
        ]

        for case in test_cases:
            job = MagicMock()
            job.departmentName = case["departmentName"]
            job.title = case["title"]
            _normalize_field(job)
            assert job.field == FieldEnum.DATA.value

    def test_normalize_field_machine_learning(self):
        test_cases = [
            "ML Engineer",
            "Machine Learning Engineer",
            "AI Developer"
        ]

        for title in test_cases:
            job = MagicMock()
            job.departmentName = "Engineering"
            job.title = title
            _normalize_field(job)
            assert job.field == FieldEnum.MACHINE_LEARNING.value

    def test_normalize_field_design(self):
        test_cases = [
            {"departmentName": "Design", "title": "Engineer"},
            {"departmentName": "Engineering", "title": "UX Designer"},
            {"departmentName": "Engineering", "title": "UI Developer"},
            {"departmentName": "Engineering", "title": "Product Designer"}
        ]

        for case in test_cases:
            job = MagicMock()
            job.departmentName = case["departmentName"]
            job.title = case["title"]
            _normalize_field(job)
            assert job.field == FieldEnum.DESIGN.value

    def test_normalize_field_product(self):
        job = MagicMock()
        job.departmentName = "Product"
        job.title = "Product Manager"
        _normalize_field(job)
        assert job.field == FieldEnum.PRODUCT.value

    def test_normalize_field_support(self):
        test_cases = [
            {"departmentName": "Support", "title": "Engineer"},
            {"departmentName": "Engineering", "title": "IT Specialist"},
            {"departmentName": "Engineering", "title": "Customer Support"}
        ]

        for case in test_cases:
            job = MagicMock()
            job.departmentName = case["departmentName"]
            job.title = case["title"]
            _normalize_field(job)
            assert job.field == FieldEnum.SUPPORT.value

    def test_normalize_field_qa(self):
        job = MagicMock()
        job.departmentName = "Engineering"
        job.title = "QA Engineer"
        _normalize_field(job)
        assert job.field == FieldEnum.QA.value

    def test_normalize_field_engineering(self):
        test_cases = [
            {"departmentName": "Engineering", "title": "Software Engineer"},
            {"departmentName": "Software Engineering", "title": "Developer"}
        ]

        for case in test_cases:
            job = MagicMock()
            job.departmentName = case["departmentName"]
            job.title = case["title"]
            _normalize_field(job)
            assert job.field == FieldEnum.ENGINEERING.value

    def test_normalize_field_engineering_excludes_hardware(self):
        job = MagicMock()
        job.departmentName = "Hardware Engineering"
        job.title = "Hardware Specialist"
        _normalize_field(job)
        assert job.field == FieldEnum.OTHER.value

    def test_normalize_field_engineering_excludes_growth_engineer(self):
        job = MagicMock()
        job.departmentName = "Marketing"
        job.title = "Growth Engineer"
        _normalize_field(job)
        assert job.field == FieldEnum.OTHER.value

    def test_normalize_field_other_default(self):
        job = MagicMock()
        job.departmentName = "Marketing"
        job.title = "Marketing Manager"
        _normalize_field(job)
        assert job.field == FieldEnum.OTHER.value

    def test_normalize_field_empty_values(self):
        job = MagicMock()
        job.departmentName = ""
        job.title = ""
        _normalize_field(job)
        assert job.field == FieldEnum.OTHER.value

    def test_normalize_field_missing_attributes(self):
        job = MagicMock()
        del job.departmentName
        del job.title
        _normalize_field(job)
        assert job.field == FieldEnum.OTHER.value

    @patch("src.services.normalize_jobs_service.friendly_job_to_normalized_job")
    @patch("src.services.normalize_jobs_service._define_url")
    def test_normalize_jobs_success(self, mock_define_url, mock_friendly_to_normalized):
        friendly_job1 = MagicMock()
        friendly_job1.id = "job-1"
        friendly_job2 = MagicMock()
        friendly_job2.id = "job-2"
        friendly_jobs = [friendly_job1, friendly_job2]

        normalized_job1 = MagicMock()
        normalized_job1.title = "Senior Engineer"
        normalized_job1.departmentName = "Engineering"

        normalized_job2 = MagicMock()
        normalized_job2.title = "Data Scientist"
        normalized_job2.departmentName = "Data"

        mock_friendly_to_normalized.side_effect = [normalized_job1, normalized_job2]
        mock_define_url.side_effect = ["url1", "url2"]

        result = normalize_jobs(friendly_jobs, "test-company")

        assert len(result) == 2
        assert normalized_job1 in result
        assert normalized_job2 in result

        assert normalized_job1.seniority_level == SeniorityEnum.SENIOR.value
        assert normalized_job1.field == FieldEnum.ENGINEERING.value
        assert normalized_job2.seniority_level == SeniorityEnum.MID_LEVEL.value
        assert normalized_job2.field == FieldEnum.DATA.value

    @patch("src.services.normalize_jobs_service.friendly_job_to_normalized_job")
    @patch("src.services.normalize_jobs_service._define_url")
    def test_normalize_jobs_empty_list(self, mock_define_url, mock_friendly_to_normalized):
        result = normalize_jobs([], "test-company")

        assert result == []
        mock_friendly_to_normalized.assert_not_called()
        mock_define_url.assert_not_called()
