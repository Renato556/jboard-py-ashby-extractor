from models.enums.company_enum import CompanyEnum
from services.jobs_service import get_jobs
import time

if __name__ == "__main__":
    start_time = time.time()
    get_jobs(CompanyEnum.COMMURE_ATHELAS)
    get_jobs(CompanyEnum.EIGHTSLEEP)
    get_jobs(CompanyEnum.SUPABASE)
    get_jobs(CompanyEnum.DEEL)
    get_jobs(CompanyEnum.POSTHOG)

    print(f'[INFO] First execution time: {time.time() - start_time} seconds')
