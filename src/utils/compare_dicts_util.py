import logging
from typing import List, Dict, Any, Tuple


logger = logging.getLogger(__name__)
Diff = Dict[str, Any]


def compare_and_diff_strict(last_list: List[Dict[str, Any]], new_list: List[Dict[str, Any]]) -> Tuple[bool, List[Diff]]:
    last_by_id = {j['id']: j for j in last_list}
    new_by_id  = {j['id']: j for j in new_list}

    last_ids = set(last_by_id.keys())
    new_ids  = set(new_by_id.keys())

    differences: List[Diff] = []

    for jid in new_ids - last_ids:
        new_job = new_by_id[jid]
        differences.append({'action': 'INSERT', 'new': new_job})
        logger.info(f'INSERT {new_job['id']}')

    for jid in last_ids - new_ids:
        last_job = last_by_id[jid]
        differences.append({'action': 'DELETE', 'old': last_job})
        logger.info(f'DELETE {last_job['id']}')

    for jid in last_ids & new_ids:
        old = last_by_id[jid]
        new = new_by_id[jid]
        if new != old:
            differences.append({'action': 'UPDATE', 'old': old, 'new': new})
            logger.info(f'UPDATE {jid}')

    are_equal = len(differences) == 0
    return are_equal, differences