import pytest
from unittest.mock import MagicMock
from src.mappers.job_mapper import (
    _dict_to_job, _dict_to_friendly_job, dicts_to_jobs,
    dicts_to_friendly_jobs, job_to_friendly_job, friendly_job_to_normalized_job,
    _clean_string
)
from src.models.job import Job
from src.models.friendly_job import FriendlyJob
from src.models.normalized_job import NormalizedJob


class TestJobMapper:
    def test_clean_string_with_spaces(self):
        assert _clean_string("  Talent Lead  ") == "Talent Lead"
        assert _clean_string("Software Engineer ") == "Software Engineer"
        assert _clean_string(" Data Scientist") == "Data Scientist"

    def test_clean_string_with_normal_string(self):
        assert _clean_string("Software Engineer") == "Software Engineer"

    def test_clean_string_with_empty_string(self):
        assert _clean_string("") == ""
        assert _clean_string("   ") == ""

    def test_clean_string_with_none(self):
        assert _clean_string(None) is None

    def test_clean_string_with_non_string(self):
        assert _clean_string(123) == 123
        assert _clean_string(True) is True
        assert _clean_string([]) == []

    def test_dict_to_job_with_spaces_in_fields(self):
        data = {
            'id': '  job-123  ',
            'title': '  Software Engineer  ',
            'departmentName': ' Engineering ',
            'locationName': '  Remote  ',
            'workplaceType': ' remote ',
            'employmentType': '  full-time  '
        }

        job = _dict_to_job(data)

        assert job.id == 'job-123'
        assert job.title == 'Software Engineer'
        assert job.departmentName == 'Engineering'
        assert job.locationName == 'Remote'
        assert job.workplaceType == 'remote'
        assert job.employmentType == 'full-time'

    def test_dict_to_job_complete_data(self):
        data = {
            'id': 'job-123',
            'title': 'Software Engineer',
            'updatedAt': '2023-01-01',
            'suppressDescriptionOpening': False,
            'suppressDescriptionClosing': True,
            'departmentId': 'dept-1',
            'departmentName': 'Engineering',
            'locationId': 'loc-1',
            'locationName': 'Remote',
            'workplaceType': 'remote',
            'employmentType': 'full-time',
            'isListed': True,
            'jobId': 'job-456',
            'jobRequisitionId': 'req-789',
            'teamId': 'team-1',
            'teamName': 'Backend',
            'publishedDate': '2023-01-01',
            'applicationDeadline': '2023-12-31',
            'shouldDisplayCompensationOnJobBoard': True,
            'secondaryLocations': ['São Paulo', 'Rio de Janeiro'],
            'compensationTierSummary': '$100k-150k',
            'userRoles': ['developer', 'engineer']
        }

        job = _dict_to_job(data)

        assert job.id == 'job-123'
        assert job.title == 'Software Engineer'
        assert job.departmentName == 'Engineering'
        assert job.locationName == 'Remote'
        assert job.secondaryLocations == ['São Paulo', 'Rio de Janeiro']
        assert job.userRoles == ['developer', 'engineer']

    def test_dict_to_job_minimal_data(self):
        data = {'id': 'job-123', 'title': 'Developer'}

        job = _dict_to_job(data)

        assert job.id == 'job-123'
        assert job.title == 'Developer'
        assert job.departmentName is None
        assert job.secondaryLocations == []
        assert job.userRoles == []

    def test_dict_to_job_empty_data(self):
        data = {}

        job = _dict_to_job(data)

        assert job.id is None
        assert job.title is None
        assert job.secondaryLocations == []
        assert job.userRoles == []

    def test_dict_to_job_null_secondary_locations(self):
        data = {'id': 'job-123', 'secondaryLocations': None}

        job = _dict_to_job(data)

        assert job.secondaryLocations == []

    def test_dict_to_job_null_user_roles(self):
        data = {'id': 'job-123', 'userRoles': None}

        job = _dict_to_job(data)

        assert job.userRoles == []

    def test_dict_to_friendly_job_with_brazilian_flag(self):
        data = {
            'id': 'job-123',
            'title': 'Software Engineer',
            'is_brazilian_friendly': True
        }

        friendly_job = _dict_to_friendly_job(data)

        assert friendly_job.id == 'job-123'
        assert friendly_job.title == 'Software Engineer'
        assert friendly_job.is_brazilian_friendly is True

    def test_dict_to_friendly_job_without_brazilian_flag(self):
        data = {'id': 'job-123', 'title': 'Software Engineer'}

        friendly_job = _dict_to_friendly_job(data)

        assert friendly_job.id == 'job-123'
        assert friendly_job.title == 'Software Engineer'
        assert friendly_job.is_brazilian_friendly is None

    def test_dicts_to_jobs_multiple_items(self):
        data = [
            {'id': 'job-1', 'title': 'Engineer 1'},
            {'id': 'job-2', 'title': 'Engineer 2'},
            {'id': 'job-3', 'title': 'Engineer 3'}
        ]

        jobs = dicts_to_jobs(data)

        assert len(jobs) == 3
        assert all(isinstance(job, Job) for job in jobs)
        assert jobs[0].id == 'job-1'
        assert jobs[1].id == 'job-2'
        assert jobs[2].id == 'job-3'

    def test_dicts_to_jobs_empty_list(self):
        jobs = dicts_to_jobs([])
        assert jobs == []

    def test_dicts_to_friendly_jobs_multiple_items(self):
        data = [
            {'id': 'job-1', 'title': 'Engineer 1', 'is_brazilian_friendly': True},
            {'id': 'job-2', 'title': 'Engineer 2', 'is_brazilian_friendly': False},
            {'id': 'job-3', 'title': 'Engineer 3'}
        ]

        friendly_jobs = dicts_to_friendly_jobs(data)

        assert len(friendly_jobs) == 3
        assert all(isinstance(job, FriendlyJob) for job in friendly_jobs)
        assert friendly_jobs[0].is_brazilian_friendly is True
        assert friendly_jobs[1].is_brazilian_friendly is False
        assert friendly_jobs[2].is_brazilian_friendly is None

    def test_dicts_to_friendly_jobs_empty_list(self):
        friendly_jobs = dicts_to_friendly_jobs([])
        assert friendly_jobs == []

    def test_job_to_friendly_job_from_job_object(self):
        job = Job(id='job-123', title='Software Engineer', updatedAt=None, suppressDescriptionOpening=None,
                  suppressDescriptionClosing=None, departmentId=None, departmentName=None, locationId=None,
                  locationName=None, workplaceType=None, employmentType=None, isListed=None, jobId=None,
                  jobRequisitionId=None, teamId=None, teamName=None, publishedDate=None, applicationDeadline=None,
                  shouldDisplayCompensationOnJobBoard=None, secondaryLocations=[], compensationTierSummary=None,
                  userRoles=[])

        friendly_job = job_to_friendly_job(job)

        assert isinstance(friendly_job, FriendlyJob)
        assert friendly_job.id == 'job-123'
        assert friendly_job.title == 'Software Engineer'
        assert friendly_job.is_brazilian_friendly is None

    def test_job_to_friendly_job_from_dict(self):
        job_dict = {'id': 'job-123', 'title': 'Software Engineer'}

        friendly_job = job_to_friendly_job(job_dict)

        assert isinstance(friendly_job, FriendlyJob)
        assert friendly_job.id == 'job-123'
        assert friendly_job.title == 'Software Engineer'
        assert friendly_job.is_brazilian_friendly is None

    def test_friendly_job_to_normalized_job_complete(self):
        friendly_job = MagicMock()
        friendly_job.id = 'job-123'
        friendly_job.title = 'Software Engineer'
        friendly_job.is_brazilian_friendly = True
        friendly_job.updatedAt = '2023-01-01'
        friendly_job.employmentType = 'full-time'
        friendly_job.publishedDate = '2023-01-01'
        friendly_job.applicationDeadline = '2023-12-31'
        friendly_job.compensationTierSummary = '$100k-150k'
        friendly_job.workplaceType = 'remote'

        normalized_job = friendly_job_to_normalized_job(
            friendly_job, 'test-company', 'https://test.com/job', 'senior', 'engineering'
        )

        assert isinstance(normalized_job, NormalizedJob)
        assert normalized_job.id == 'job-123'
        assert normalized_job.title == 'Software Engineer'
        assert normalized_job.is_brazilian_friendly is True
        assert normalized_job.company == 'test-company'
        assert normalized_job.url == 'https://test.com/job'
        assert normalized_job.seniority_level == 'senior'
        assert normalized_job.field == 'engineering'
        assert normalized_job.office_location is None

    def test_friendly_job_to_normalized_job_minimal(self):
        friendly_job = MagicMock()

        normalized_job = friendly_job_to_normalized_job(
            friendly_job, 'test-company', 'https://test.com/job', None, None
        )

        assert isinstance(normalized_job, NormalizedJob)
        assert normalized_job.company == 'test-company'
        assert normalized_job.url == 'https://test.com/job'
        assert normalized_job.seniority_level is None
        assert normalized_job.field is None
        assert normalized_job.office_location is None

    def test_friendly_job_to_normalized_job_with_spaces(self):
        friendly_job = MagicMock()
        friendly_job.id = '  job-123  '
        friendly_job.title = '  Software Engineer  '
        friendly_job.updatedAt = '  2023-01-01  '
        friendly_job.employmentType = '  full-time  '
        friendly_job.workplaceType = '  remote  '

        normalized_job = friendly_job_to_normalized_job(
            friendly_job, '  test-company  ', '  https://test.com/job  ', '  senior  ', '  engineering  '
        )

        assert normalized_job.id == 'job-123'
        assert normalized_job.title == 'Software Engineer'
        assert normalized_job.updated_at == '2023-01-01'
        assert normalized_job.employment_type == 'full-time'
        assert normalized_job.workplace_type == 'remote'
        assert normalized_job.company == 'test-company'
        assert normalized_job.url == 'https://test.com/job'
        assert normalized_job.seniority_level == 'senior'
        assert normalized_job.field == 'engineering'
