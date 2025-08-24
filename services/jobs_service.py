import json
import logging
from typing import List, Any

from models.enums.company_enum import CompanyEnum
from models.normalized_job import NormalizedJob
from services.fetch_jobs_service import fetch_jobs
from services.filter_jobs_service import filter_brazilian_friendly_jobs
from services.normalize_jobs_service import normalize_jobs
from utils.compare_dicts_util import compare_and_diff_strict

logger = logging.getLogger(__name__)

def _check_file_exists(filename: str) -> None:
    try:
        with open(filename, 'r') as file:
            file.read()
    except FileNotFoundError:
        open(filename, 'x')


def _compare_to_last_execution(company: CompanyEnum, new_execution: List[NormalizedJob]) -> list[dict[str, Any]]:
    filename = f'last_{company.value}.json'

    _check_file_exists(filename)

    with open(filename, 'r') as file:
        last_execution = file.read()

    if last_execution == '':
        last_execution = json.dumps([])

    list_dict_last_execution = json.loads(last_execution)
    list_dict_new_execution = [new_execution.to_dict() for new_execution in new_execution]

    are_equal, differences = compare_and_diff_strict(list_dict_last_execution, list_dict_new_execution)

    if are_equal:
        logger.info(f'No new jobs for company: {company}')
        return []
    logger.info(f'Differences found for company: {company} | Differences found: {len(differences)}')

    json_new_execution = json.dumps(list_dict_new_execution)

    with open(filename, 'w') as file:
        file.write(json_new_execution)
    return differences


def get_jobs(company: CompanyEnum) -> None:
    all_job_listings = fetch_jobs(company)

    if not all_job_listings:
        return

    brazilian_friendly_jobs = filter_brazilian_friendly_jobs(all_job_listings, company)
    logger.info(f'Filtered brazilian friendly jobs for company: {company} | Jobs found: {len(brazilian_friendly_jobs)}')
    normalized_jobs = normalize_jobs(brazilian_friendly_jobs, company)
    differences = _compare_to_last_execution(company, normalized_jobs)
    # POSTAR NA FILA

