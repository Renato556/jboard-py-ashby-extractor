import os
import logging

import requests

logger = logging.getLogger(__name__)

def insert_job(job):
    response = requests.post(f'{os.getenv('API_URL')}/jobs', json=job)

    if response.status_code == 304:
        logger.info(f'Job already exists in database: {job}')
        return
    elif not response.ok:
        raise Exception('Error inserting job')

    logger.info(f'Job successfully inserted in database: {job}')


def update_job(job):
    response = requests.put(f'{os.getenv('API_URL')}/jobs', json=job)

    if response.status_code == 404:
        logger.info(f'Job does not exist in database: {job}')
        return
    elif not response.ok:
        raise Exception('Error updating job')

    logger.info(f'Job successfully updated in database: {job}')


def delete_job(job):
    response = requests.delete(f'{os.getenv('API_URL')}/{job['url']}')

    if response.status_code == 404:
        logger.info(f'Job does not exist in database: {job}')
        return
    elif not response.ok:
        raise Exception('Error deleting job')

    logger.info(f'Job successfully deleted in database: {job}')