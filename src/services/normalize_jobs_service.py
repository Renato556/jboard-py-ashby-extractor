import logging
import os
from typing import List

from src.mappers.job_mapper import friendly_job_to_normalized_job
from src.models.enums.field_enum import FieldEnum
from src.models.enums.seniority_enum import SeniorityEnum
from src.models.friendly_job import FriendlyJob
from src.models.normalized_job import NormalizedJob


logger = logging.getLogger(__name__)


def _define_url(company: str, job_id: str) -> str:
    return f'{os.getenv('DEFAULT_URL')}{company.replace(' ', '%20')}/{job_id}'


def _set_seniority(job: NormalizedJob, seniority: SeniorityEnum) -> None:
    setattr(job, 'seniority_level', seniority.value)


def _normalize_seniority(job: NormalizedJob) -> None:
    title_lower = getattr(job, 'title', '').lower()

    if ('staff' in title_lower or 'director' in title_lower or 'head' in title_lower  or ('manager' in title_lower and 'senior' not in title_lower) or
            ('lead' in title_lower and not 'tech lead' in title_lower and not 'team lead' in title_lower)):
        _set_seniority(job, SeniorityEnum.STAFF)
    elif 'senior' in title_lower or 'sr.' in title_lower or 'lead' in title_lower or 'architect' in title_lower or 'expert' in title_lower:
        _set_seniority(job, SeniorityEnum.SENIOR)
    elif 'junior' in title_lower or 'entry_level' in title_lower or 'associate' in title_lower:
        _set_seniority(job, SeniorityEnum.JUNIOR)
    elif 'intern' in title_lower:
        _set_seniority(job, SeniorityEnum.INTERN)
    else:
        _set_seniority(job, SeniorityEnum.MID_LEVEL)


def _set_field(job: NormalizedJob, field: str) -> None:
    setattr(job, 'field', field)


def _normalize_field(job: NormalizedJob) -> None:
    department_lower = getattr(job, 'departmentName', '').lower()
    title_lower = getattr(job, 'title', '').lower()

    if 'data' in department_lower or 's&m' in department_lower or 'data scientist' in title_lower:
        _set_field(job, FieldEnum.DATA.value)
    elif 'ml' in title_lower or 'machine learning' in title_lower or 'ai' in title_lower:
        _set_field(job, FieldEnum.MACHINE_LEARNING.value)
    elif 'design' in department_lower or 'ux' in title_lower or 'ui' in title_lower or 'design' in title_lower:
        _set_field(job, FieldEnum.DESIGN.value)
    elif 'product' in department_lower:
        _set_field(job, FieldEnum.PRODUCT.value)
    elif 'support' in department_lower or 'it ' in title_lower or 'support' in title_lower:
        _set_field(job, FieldEnum.SUPPORT.value)
    elif 'qa' in title_lower:
        _set_field(job, FieldEnum.QA.value)
    elif ('engineering' in department_lower and not 'hardware' in department_lower) or ('engineer' in title_lower and not 'growth' in title_lower):
        _set_field(job, FieldEnum.ENGINEERING.value)
    else:
        _set_field(job, FieldEnum.OTHER.value)


def normalize_jobs(jobs: List[FriendlyJob], company: str) -> List[NormalizedJob]:
    normalized_jobs = []
    for job in jobs:
        normalized_job = friendly_job_to_normalized_job(job, company, _define_url(company, getattr(job, 'id')), None, None)
        _normalize_seniority(normalized_job)
        _normalize_field(normalized_job)
        normalized_jobs.append(normalized_job)
    logger.info(f'Normalized jobs for company: {company}')

    return normalized_jobs