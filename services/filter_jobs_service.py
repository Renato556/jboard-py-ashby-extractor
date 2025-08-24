import logging
from typing import Any, List

from models.job import Job
from models.friendly_job import FriendlyJob
from models.enums.company_enum import CompanyEnum
from mappers.job_mapper import job_to_friendly_job

logger = logging.getLogger(__name__)

IS_BRAZILIAN_FRIENDLY_KEY = 'is_brazilian_friendly'

REASON_GLOBAL_TITLE_OR_LOCATION = '[global_filter] Brazil in title or location'
REASON_GLOBAL_SECONDARY_LOCATION = '[global_filter] Brazil in secondary location'
REASON_GLOBAL_DEFAULT = 'global_filter'

REASON_EIGHTSLEEP_MATCH = '[eightsleep_filter] LATAM in location'
REASON_EIGHTSLEEP_DEFAULT = 'eightsleep_filter'

REASON_SUPABASE_MATCH = '[supabase_filter] Location remote and specific to americas or global'
REASON_SUPABASE_DEFAULT = 'supabase_filter'

REASON_DEEL_MATCH = '[deel_filter] Anywhere (LATAM) in location'
REASON_DEEL_DEFAULT = 'deel_filter'


def _lower(value: str | None) -> str:
    return (value or '').strip().lower()


def _attr_or_key(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _mark_brazilian_friendly(job_listing: FriendlyJob, is_friendly: bool, reason: str) -> None:
    setattr(job_listing, IS_BRAZILIAN_FRIENDLY_KEY, {'isFriendly': is_friendly, 'reason': reason})


def _global_filter(job_listing: FriendlyJob) -> bool:
    title_lower = _lower(getattr(job_listing, 'title', None))
    location_lower = _lower(getattr(job_listing, 'locationName', None))

    if 'brazil' in title_lower or 'brazil' in location_lower:
        _mark_brazilian_friendly(job_listing, True, REASON_GLOBAL_TITLE_OR_LOCATION)
        return True

    secondary_locations = getattr(job_listing, 'secondaryLocations', None) or []
    for location in secondary_locations:
        if 'brazil' in _lower(_attr_or_key(location, 'locationName')):
            _mark_brazilian_friendly(job_listing, True, REASON_GLOBAL_SECONDARY_LOCATION)
            return True

    _mark_brazilian_friendly(job_listing, False, REASON_GLOBAL_DEFAULT)
    return False


def _eightsleep_filter(job_listing: FriendlyJob) -> bool:
    location_lower = _lower(getattr(job_listing, 'locationName', None))
    if 'latam' in location_lower:
        _mark_brazilian_friendly(job_listing, True, REASON_EIGHTSLEEP_MATCH)
        return True
    _mark_brazilian_friendly(job_listing, False, REASON_EIGHTSLEEP_DEFAULT)
    return False


def _supabase_filter(job_listing: FriendlyJob) -> bool:
    title_lower = _lower(getattr(job_listing, 'title', None))
    location_lower = _lower(getattr(job_listing, 'locationName', None))

    is_americas = 'americas' in title_lower or 'us time zones' in title_lower
    is_global_remote = ('(' not in title_lower) and (location_lower == 'remote')

    if is_americas or is_global_remote:
        _mark_brazilian_friendly(job_listing, True, REASON_SUPABASE_MATCH)
        return True

    _mark_brazilian_friendly(job_listing, False, REASON_SUPABASE_DEFAULT)
    return False


def _deel_filter(job_listing: FriendlyJob) -> bool:
    if 'anywhere (latam)' in _lower(getattr(job_listing, 'locationName', None)):
        _mark_brazilian_friendly(job_listing, True, REASON_DEEL_MATCH)
        return True
    _mark_brazilian_friendly(job_listing, False, REASON_DEEL_DEFAULT)
    return False


def _filter_by_company(job_listing: FriendlyJob, company: CompanyEnum) -> bool:
    if _global_filter(job_listing):
        return True

    if company == CompanyEnum.EIGHTSLEEP:
        return _eightsleep_filter(job_listing)
    elif company == CompanyEnum.SUPABASE:
        return _supabase_filter(job_listing)
    elif company == CompanyEnum.DEEL:
        return _deel_filter(job_listing)

    return False


def filter_brazilian_friendly_jobs(jobs: List[Job], company: CompanyEnum) -> List[FriendlyJob]:
    logger.info(f'Filtering brazilian friendly jobs for company: {company}')

    brazilian_friendly_jobs: List[FriendlyJob] = []

    for job in jobs:
        mapped_job = job_to_friendly_job(job)
        if _filter_by_company(mapped_job, company):
            brazilian_friendly_jobs.append(mapped_job)

    return brazilian_friendly_jobs