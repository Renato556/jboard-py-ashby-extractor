import logging
import os
import time
import schedule
from dotenv import load_dotenv

from src.services.jobs_service import get_jobs

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def _run() -> None:
    companies = os.getenv('COMPANIES').split(',')
    logger.info('Running application')

    for company in companies:
        get_jobs(company)
        time.sleep(3)


def main() -> None:
    logger.info('Starting application')
    _run()
    schedule.every(int(os.getenv('TIME_BETWEEN_EXECUTIONS'))).minutes.do(_run)


if __name__ == '__main__':
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
