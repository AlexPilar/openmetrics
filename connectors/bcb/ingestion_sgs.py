import requests
import json
from pathlib import Path
import pandas as pd
from utils.logger import logger

RAW_PATH = Path("data/raw")
CATALOG_PATH = Path("openmetrics_dbt/seeds/indicators.csv")

START_DATE = "01/01/2026"
END_DATE = "30/06/2026"

RAW_PATH.mkdir(parents=True, exist_ok=True)

REQUEST_TIMEOUT = 30


catalog = pd.read_csv(CATALOG_PATH)

logger.info("Starting BCB ingestion...")

for _, row in catalog.iterrows():
    indicator_name = row["indicator"]
    series_id = row["series_id"]

    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}"
        f"/dados?formato=json"
        f"&dataInicial={START_DATE}"
        f"&dataFinal={END_DATE}"
    )
    try:
        logger.info(f"Fetching {indicator_name}...")
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"{indicator_name}: erro ao acessar a API - {e}")
        continue

    data = response.json()

    if not data:
        logger.warning(f"{indicator_name}: nenhum registro retornado.")
        continue

    output_file = RAW_PATH / f"{indicator_name}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logger.info(f"{indicator_name}: {len(data)} registros salvos em {output_file}")

logger.info("BCB ingestion finished successfully.")
