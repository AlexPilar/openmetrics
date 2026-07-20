import json
from pathlib import Path

import pandas as pd
import requests

from utils.logger import logger

RAW_PATH = Path("data/raw")
CATALOG_PATH = Path("openmetrics_dbt/seeds/indicators.csv")

START_DATE = "01/01/2026"
END_DATE = "30/06/2026"

REQUEST_TIMEOUT = 30

RAW_PATH.mkdir(parents=True, exist_ok=True)

def build_url(series_id:int) -> str:
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}"
        f"/dados?formato=json"
        f"&dataInicial={START_DATE}"
        f"&dataFinal={END_DATE}"
    )
    return url

def fetch_data(indicator_name, url):
    logger.info(f"Fetching {indicator_name}...")

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"{indicator_name}: erro ao acessar a API - {e}")
        return None

def save_json(data: list, indicator_name: str) -> bool:
    if not data:
        logger.warning(f"{indicator_name}: nenhum registro retornado.")
        return False

    output_file = RAW_PATH / f"{indicator_name}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logger.info(f"{indicator_name}: {len(data)} registros salvos em {output_file}")
    return True

def main():
    logger.info("Starting BCB ingestion...")
    catalog = pd.read_csv(CATALOG_PATH)

    for _, row in catalog.iterrows():
        indicator_name = row["indicator"]
        series_id = row["series_id"]

        url = build_url(series_id)

        data = fetch_data(indicator_name, url)

        if data is None:
            continue

        save_json(data, indicator_name)
        
    logger.info("BCB ingestion finished successfully.")

if __name__ == "__main__":
    main()
    