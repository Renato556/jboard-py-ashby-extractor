import re
import json
from typing import List

from mappers.job_mapper import dicts_to_jobs
from models.enums.company_enum import CompanyEnum
from clients import ashby_client
from models.job import Job

def fetch_jobs(company: CompanyEnum) -> List[Job] | None:
    response = ashby_client.fetch_listings(company)
    
    if response:
        data = re.search(r'window\.__appData\s*=\s*({.*?});', response)
    
        if data:
            json_string = data.group(1)
            app_data = json.loads(json_string)

            print(f'[INFO] Jobs sucessfully extracted for company: {company} | Total jobs: {len(app_data['jobBoard']['jobPostings'])}')
            job_postings = app_data['jobBoard']['jobPostings']
            jobs: List[Job] = dicts_to_jobs(job_postings)
            return jobs
    return None
