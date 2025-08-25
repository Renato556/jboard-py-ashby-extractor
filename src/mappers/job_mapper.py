from typing import Any, Iterable, List, Mapping, Union
from src.models.job import Job
from src.models.friendly_job import FriendlyJob
from src.models.normalized_job import NormalizedJob


def _dict_to_job(data: Mapping[str, Any]) -> Job:
    return Job(
        id=data.get('id'),
        title=data.get('title'),
        updatedAt=data.get('updatedAt'),
        suppressDescriptionOpening=data.get('suppressDescriptionOpening'),
        suppressDescriptionClosing=data.get('suppressDescriptionClosing'),
        departmentId=data.get('departmentId'),
        departmentName=data.get('departmentName'),
        locationId=data.get('locationId'),
        locationName=data.get('locationName'),
        workplaceType=data.get('workplaceType'),
        employmentType=data.get('employmentType'),
        isListed=data.get('isListed'),
        jobId=data.get('jobId'),
        jobRequisitionId=data.get('jobRequisitionId'),
        teamId=data.get('teamId'),
        teamName=data.get('teamName'),
        publishedDate=data.get('publishedDate'),
        applicationDeadline=data.get('applicationDeadline'),
        shouldDisplayCompensationOnJobBoard=data.get('shouldDisplayCompensationOnJobBoard'),
        secondaryLocations=data.get('secondaryLocations') or [],
        compensationTierSummary=data.get('compensationTierSummary'),
        userRoles=data.get('userRoles') or [],
    )


def _dict_to_friendly_job(data: Mapping[str, Any]) -> FriendlyJob:
    job = _dict_to_job(data)
    return FriendlyJob(job, data.get('is_brazilian_friendly'))


def dicts_to_jobs(items: Iterable[Mapping[str, Any]]) -> List[Job]:
    return [_dict_to_job(item) for item in items]


def dicts_to_friendly_jobs(items: Iterable[Mapping[str, Any]]) -> List[FriendlyJob]:
    return [_dict_to_friendly_job(item) for item in items]


def job_to_friendly_job(job: Union[Job, Mapping[str, Any]]) -> FriendlyJob:
    if isinstance(job, dict):
        job = _dict_to_job(job)
    return FriendlyJob(job, None)


def friendly_job_to_normalized_job(friendly_job: FriendlyJob, company: str, url: str, seniority_level: str | None, field: str | None) -> NormalizedJob:
    return NormalizedJob(
        id=getattr(friendly_job, 'id', None),
        title=getattr(friendly_job, 'title', None),
        is_brazilian_friendly=getattr(friendly_job, 'is_brazilian_friendly', None),
        updated_at=getattr(friendly_job, 'updatedAt', None),
        employment_type=getattr(friendly_job, 'employmentType', None),
        published_date=getattr(friendly_job, 'publishedDate', None),
        application_deadline=getattr(friendly_job, 'applicationDeadline', None),
        compensation_tier_summary=getattr(friendly_job, 'compensationTierSummary', None),
        workplace_type=getattr(friendly_job, 'workplaceType', None),
        office_location=None,
        company=company,
        url=url,
        seniority_level=seniority_level,
        field=field
    )