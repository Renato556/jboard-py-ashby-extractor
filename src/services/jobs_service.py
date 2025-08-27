import json
import logging
from typing import List, Any

from src.clients.database_client import insert_job, update_job, delete_job
from src.models.normalized_job import NormalizedJob
from src.services.fetch_jobs_service import fetch_jobs
from src.services.filter_jobs_service import filter_brazilian_friendly_jobs
from src.services.normalize_jobs_service import normalize_jobs
from src.utils.compare_dicts_util import compare_and_diff_strict

logger = logging.getLogger(__name__)

def _convert_job_to_json(job) -> dict[str, Any]:
    str_job = json.dumps(job)
    return json.loads(str_job)

def _check_file_exists(filename: str) -> None:
    try:
        with open(filename, 'r') as file:
            file.read()
    except FileNotFoundError:
        open(filename, 'x')


def _compare_to_last_execution(company: str, new_execution: List[NormalizedJob]) -> list[dict[str, Any]]:
    filename = f'last_{company}.json'

    _check_file_exists(filename)

    with open(filename, 'r') as file:
        last_execution = file.read()

    if last_execution == '':
        last_execution = json.dumps([])

    list_dict_last_execution = json.loads(last_execution)
    list_dict_new_execution = [item.to_dict() for item in new_execution]

    are_equal, differences = compare_and_diff_strict(list_dict_last_execution, list_dict_new_execution)

    if are_equal:
        logger.info(f'No new jobs for company: {company}')
        return []
    logger.info(f'Differences found for company: {company} | Differences found: {len(differences)}')

    for job in differences:
        json_job = _convert_job_to_json(job)
        if job['action'] == 'INSERT':
            insert_job(json_job)
        elif job['action'] == 'UPDATE':
            update_job(json_job)
        elif job['action'] == 'DELETE':
            delete_job(json_job)

    json_new_execution = json.dumps(list_dict_new_execution)

    with open(filename, 'w') as file:
        file.write(json_new_execution)
    return differences


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

    differences = _compare_to_last_execution(company, normalized_jobs)

    # POSTAR NA FILA

