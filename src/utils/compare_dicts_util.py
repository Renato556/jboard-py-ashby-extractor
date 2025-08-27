import logging
from typing import List, Dict, Any, Tuple


logger = logging.getLogger(__name__)
Diff = Dict[str, Any]


def compare_and_diff_strict(last_list: List[Dict[str, Any]], new_list: List[Dict[str, Any]]) -> Tuple[bool, List[Diff]]:
    last_by_id = {j['url']: j for j in last_list}
    new_by_id  = {j['url']: j for j in new_list}

    last_urls = set(last_by_id.keys())
    new_urls  = set(new_by_id.keys())

    differences: List[Diff] = []

    for url in new_urls - last_urls:
        new_job = new_by_id[url]
        new_job = {**new_job, 'action': 'INSERT'}
        differences.append(new_job)
        logger.info(f'INSERT {new_job['url']}')

    for url in last_urls - new_urls:
        last_job = last_by_id[url]
        last_job = {**last_job, 'action': 'DELETE'}
        differences.append(last_job)
        logger.info(f'DELETE {last_job['url']}')

    for url in last_urls & new_urls:
        old = last_by_id[url]
        new = new_by_id[url]
        if new != old:
            new = {**new, 'action': 'UPDATE'}
            differences.append(new)
            logger.info(f'UPDATE {url}')

    are_equal = len(differences) == 0
    return are_equal, differences