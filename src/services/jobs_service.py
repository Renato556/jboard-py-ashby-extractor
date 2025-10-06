import logging

from src.clients.database_client import insert_job
from src.services.fetch_jobs_service import fetch_jobs
from src.services.filter_jobs_service import filter_brazilian_friendly_jobs
from src.services.normalize_jobs_service import normalize_jobs

logger = logging.getLogger(__name__)

def _save_to_db(jobs) -> None:
    for job in jobs:
        insert_job(job.to_dict())

def get_jobs(company: str) -> None:
    all_job_listings = fetch_jobs(company)

    if not all_job_listings:
        logger.info(f'No listings returned for company: {company}')
        return

    brazilian_friendly_jobs = filter_brazilian_friendly_jobs(all_job_listings, company)
    if not brazilian_friendly_jobs:
        logger.info(f'No brazilian friendly jobs for company: {company}')
        return

    logger.info(f'Filtered brazilian friendly jobs for company: {company} | Jobs found: {len(brazilian_friendly_jobs)}')
    normalized_jobs = normalize_jobs(brazilian_friendly_jobs, company)

    if not normalized_jobs:
        logger.info(f'No normalized jobs for company: {company}')
        return

    logger.info(f'Saving {len(normalized_jobs)} jobs to database for company: {company}')

    try:
        _save_to_db(normalized_jobs)
        logger.info(f'Successfully saved jobs to database for company: {company}')
    except Exception as e:
        logger.exception(f'Error saving jobs to database for company: {company} | Error: {e}')
        raise
