import requests
import os
import logging
from dotenv import load_dotenv

from requests import RequestException

load_dotenv()
logger = logging.getLogger(__name__)

def fetch_listings(company: str) -> str | None:
    timeout = float(os.getenv('ASHBY_TIMEOUT'))

    try:
        logger.info(f'Fetching jobs from ashby for company: {company}')
        response = requests.get(os.getenv('DEFAULT_URL') + company, timeout=timeout)

        if response.ok:
            logger.info(f'Jobs successfully fetched for company: {company}')
            return response.text
        else:
            logger.info(f'Error getting jobs from ashby for company: {company} | Status code: {response.status_code}')
            return None
    except RequestException as e:
        logger.error(f'[RequestException] Error getting jobs from ashby for company: {company} | Error {e}')
        return None
    except Exception as e:
        logger.exception(f'[UnexpectedException] Error getting jobs from ashby for company: {company} | Error {e}')
        return None
