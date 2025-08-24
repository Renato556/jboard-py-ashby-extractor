import json
from typing import List, Any

from models.enums.company_enum import CompanyEnum
from models.friendly_job import FriendlyJob
from services.fetch_jobs_service import fetch_jobs
from services.filter_jobs_service import filter_brazilian_friendly_jobs
from utils.compare_dicts_util import compare_and_diff_strict


def _check_file_exists(filename: str) -> None:
    try:
        with open(filename, 'r') as file:
            file.read()
    except FileNotFoundError:
        open(filename, 'x')


def _compare_to_last_execution(company: CompanyEnum, new_execution: List[FriendlyJob]) -> list[dict[str, Any]]:
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
        print(f'[INFO] No new jobs for company: {company.value}')
        return []

    json_new_execution = json.dumps(list_dict_new_execution)

    with open(filename, 'w') as file:
        file.write(json_new_execution)
    return differences


def get_jobs(company: CompanyEnum) -> None:
    # TODO: Chamar get_jobs_service, filter_jobs_service, normalize_jobs_service e o service que poste numa fila para a outra aplicação salvar no banco
    all_job_listings = fetch_jobs(company)
    brazilian_friendly_jobs = filter_brazilian_friendly_jobs(all_job_listings, company)
    print(f'[INFO] Brazilian friendly jobs for company: {company.value} | Total jobs: {len(brazilian_friendly_jobs)}')
    # NORMALIZE FIRST
    differences = _compare_to_last_execution(company, brazilian_friendly_jobs)
    # POSTAR NA FILA

