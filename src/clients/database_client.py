import os
import logging
from typing import Optional

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class DatabaseClient:
    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.timeout = int(os.getenv('API_TIMEOUT', '30'))
        self.session = self._create_session()

        if not self.api_url:
            raise ValueError("API_URL environment variable is required but not set")

    def _create_session(self) -> requests.Session:
        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'ashby-job-extractor/1.0'
        })

        return session

    def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> Response:
        url = f'{self.api_url}/{endpoint.lstrip("/")}'

        try:
            logger.debug(f'Making {method} request to {url}')
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout
            )

            logger.debug(f'Response status: {response.status_code}')
            return response

        except requests.exceptions.Timeout:
            logger.error(f'API timeout after {self.timeout} seconds: {url}')
            raise Exception(f'API timeout after {self.timeout} seconds')
        except requests.exceptions.ConnectionError:
            logger.error(f'Failed to connect to API - check network connectivity: {url}')
            raise Exception('Failed to connect to API - check network connectivity')
        except requests.exceptions.RequestException as e:
            logger.error(f'Request failed: {url}: {e}')
            raise Exception(f'Request failed: {e}')

_client = DatabaseClient()

def insert_job(job):
    response = _client._make_request('POST', 'jobs', job)

    if response.status_code == 304:
        logger.info(f'Job already exists in database: {job.get("title", "Unknown")}')
        return
    elif response.status_code == 201:
        logger.info(f'Job successfully inserted in database: {job.get("title", "Unknown")}')
        return
    elif not response.ok:
        logger.error(f'Error inserting job: {response.status_code} - {response.text}')
        raise Exception(f'Error inserting job: {response.status_code}')
