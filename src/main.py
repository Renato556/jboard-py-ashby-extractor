import logging
import os
import time
import json
from dotenv import load_dotenv

from src.services.jobs_service import get_jobs

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def run() -> None:
    companies_json = os.getenv('COMPANIES')
    companies_data = json.loads(companies_json)
    companies = companies_data['companies']
    logger.info('Starting job extraction process')

    for company in companies:
        company = company.strip()
        logger.info(f'Processing company: {company}')
        get_jobs(company)
        time.sleep(3)
    
    logger.info('Job extraction process completed successfully')


def main() -> None:
    try:
        run()
    except Exception as e:
        logger.exception(f'Error during job extraction: {e}')


if __name__ == '__main__':
    main()
