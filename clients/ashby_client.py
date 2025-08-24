import requests
from dotenv import load_dotenv
import os

from models.enums.company_enum import CompanyEnum

load_dotenv()

def fetch_listings(company: CompanyEnum) -> str | None:
    try:
        response = requests.get(os.getenv('DEFAULT_URL') + company.value)

        if response.status_code == 200:
            print(f'[INFO] Jobs sucessfully fetched for company: {company}')
            return response.text
        else:
            print(f'[ERROR] Error getting jobs from ashby for company: {company}')
            return None
    except Exception: # TODO: Mapear exceptions, e salvar os erros em uma tabela (catch aqui? acho que melhor na camada mais externa)
        print(f'[ERROR] Error getting jobs from ashby for company: {company}')