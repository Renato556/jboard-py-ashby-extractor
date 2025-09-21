from src.models.normalized_job import NormalizedJob


class TestNormalizedJobToDict:
    def test_normalized_job_to_dict_complete(self):
        normalized_job = NormalizedJob(
            id='job-123',
            title='Senior Software Engineer',
            updated_at='2023-01-01T10:00:00Z',
            employment_type='full-time',
            published_date='2023-01-01',
            application_deadline='2023-12-31',
            compensation_tier_summary='$120k-180k',
            workplace_type='remote',
            office_location='São Paulo, Brazil',
            is_brazilian_friendly={'reason': 'global_filter', 'match': 'Brazil in location'},
            company='test-company',
            url='https://jobs.test.com/job-123',
            seniority_level='senior',
            field='engineering'
        )

        result = normalized_job.to_dict()

        expected_dict = {
            'id': 'job-123',
            'title': 'Senior Software Engineer',
            'updatedAt': '2023-01-01T10:00:00Z',
            'employmentType': 'full-time',
            'publishedDate': '2023-01-01',
            'applicationDeadline': '2023-12-31',
            'compensationTierSummary': '$120k-180k',
            'workplaceType': 'remote',
            'officeLocation': 'São Paulo, Brazil',
            'isBrazilianFriendly': {'reason': 'global_filter', 'match': 'Brazil in location'},
            'company': 'test-company',
            'url': 'https://jobs.test.com/job-123',
            'seniorityLevel': 'senior',
            'field': 'engineering'
        }

        assert result == expected_dict
