from typing import Any, Iterable, List, Mapping, Union
from src.models.job import Job
from src.models.friendly_job import FriendlyJob
from src.models.normalized_job import NormalizedJob


def _clean_string(value: Any) -> Any:
    """Remove espaços em branco do início e fim de strings"""
    if isinstance(value, str):
        return value.strip()
    return value


def _dict_to_job(data: Mapping[str, Any]) -> Job:
    return Job(
        id=_clean_string(data.get('id')),
        title=_clean_string(data.get('title')),
        updatedAt=_clean_string(data.get('updatedAt')),
        suppressDescriptionOpening=data.get('suppressDescriptionOpening'),
        suppressDescriptionClosing=data.get('suppressDescriptionClosing'),
        departmentId=_clean_string(data.get('departmentId')),
        departmentName=_clean_string(data.get('departmentName')),
        locationId=_clean_string(data.get('locationId')),
        locationName=_clean_string(data.get('locationName')),
        workplaceType=_clean_string(data.get('workplaceType')),
        employmentType=_clean_string(data.get('employmentType')),
        isListed=data.get('isListed'),
        jobId=_clean_string(data.get('jobId')),
        jobRequisitionId=_clean_string(data.get('jobRequisitionId')),
        teamId=_clean_string(data.get('teamId')),
        teamName=_clean_string(data.get('teamName')),
        publishedDate=_clean_string(data.get('publishedDate')),
        applicationDeadline=_clean_string(data.get('applicationDeadline')),
        shouldDisplayCompensationOnJobBoard=_clean_string(data.get('shouldDisplayCompensationOnJobBoard')),
        secondaryLocations=data.get('secondaryLocations') or [],
        compensationTierSummary=_clean_string(data.get('compensationTierSummary')),
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
        id=_clean_string(getattr(friendly_job, 'id', None)),
        title=_clean_string(getattr(friendly_job, 'title', None)),
        is_brazilian_friendly=getattr(friendly_job, 'is_brazilian_friendly', None),
        updated_at=_clean_string(getattr(friendly_job, 'updatedAt', None)),
        employment_type=_clean_string(getattr(friendly_job, 'employmentType', None)),
        published_date=_clean_string(getattr(friendly_job, 'publishedDate', None)),
        application_deadline=_clean_string(getattr(friendly_job, 'applicationDeadline', None)),
        compensation_tier_summary=_clean_string(getattr(friendly_job, 'compensationTierSummary', None)),
        workplace_type=_clean_string(getattr(friendly_job, 'workplaceType', None)),
        office_location=None,
        company=_clean_string(company),
        url=_clean_string(url),
        seniority_level=_clean_string(seniority_level),
        field=_clean_string(field)
    )