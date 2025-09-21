from src.models.friendly_job import FriendlyJob
from src.models.job import Job


class TestFriendlyJobToDict:
    def test_friendly_job_to_dict(self):
        job = Job(
            id='job-123',
            title='Software Engineer',
            updatedAt='2023-01-01',
            suppressDescriptionOpening=False,
            suppressDescriptionClosing=True,
            departmentId='dept-1',
            departmentName='Engineering',
            locationId='loc-1',
            locationName='Remote',
            workplaceType='remote',
            employmentType='full-time',
            isListed=True,
            jobId='job-456',
            jobRequisitionId='req-789',
            teamId='team-1',
            teamName='Backend',
            publishedDate='2023-01-01',
            applicationDeadline='2023-12-31',
            shouldDisplayCompensationOnJobBoard='yes',
            secondaryLocations=['São Paulo'],
            compensationTierSummary='$100k-150k',
            userRoles=['developer']
        )

        friendly_job = FriendlyJob(job, {'reason': 'test', 'match': True})
        result = friendly_job.to_dict()

        assert result['id'] == 'job-123'
        assert result['title'] == 'Software Engineer'
        assert result['departmentName'] == 'Engineering'
        assert result['is_brazilian_friendly'] == {'reason': 'test', 'match': True}
