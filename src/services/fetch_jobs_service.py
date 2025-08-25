import re
import json
import logging
from typing import List, Optional

from src.mappers.job_mapper import dicts_to_jobs
from src.clients import ashby_client
from src.models.job import Job

logger = logging.getLogger(__name__)

APP_DATA_REGEX = re.compile(r'window\.__appData\s*=\s*({.*?});', re.DOTALL)

def fetch_jobs(company: str) -> Optional[List[Job]]:
    response = ashby_client.fetch_listings(company)
    if not response:
        logger.warning(f'No response content to extract for company: {company}')
        return None

    match = APP_DATA_REGEX.search(response)
    if not match:
        logger.warning(f'App data not found in page for company: {company}')
        return None

    json_string = match.group(1)

    try:
        app_data = json.loads(json_string)
        job_postings = app_data['jobBoard']['jobPostings']
    except json.JSONDecodeError as e:
        logger.error(f'Failed to parse app data JSON for company: {company} | Error: {e}')
        return None
    except (KeyError, TypeError) as e:
        logger.error(f'Unexpected app data structure for company: {company} | Error: {e}')
        return None

    jobs: List[Job] = dicts_to_jobs(job_postings)
    logger.info(f'Jobs successfully extracted for company: {company} | Total jobs: {len(jobs)}')
    return jobs