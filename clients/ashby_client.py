import requests
import os
import logging

from requests import RequestException

from models.enums.company_enum import CompanyEnum

logger = logging.getLogger(__name__)

def fetch_listings(company: CompanyEnum) -> str | None:
    try:
        logger.info(f'Fetching jobs from ashby for company: {company}')
        response = requests.get(os.getenv('DEFAULT_URL') + company.value)

        if response.status_code == 200:
            logger.info(f'Jobs successfully fetched for company: {company}')
            return response.text
        else:
            logger.info(f'Error getting jobs from ashby for company: {company} | Status code: {response.status_code}')
            return None
    except RequestException as e:
        logger.error(f'[RequestException] Error getting jobs from ashby for company: {company} | Error {e}')
        return None