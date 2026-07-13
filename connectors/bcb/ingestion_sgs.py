import requests
import json
from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw")
CATALOG_PATH = Path("openmetrics_dbt/seeds/indicators.csv")

START_DATE = "01/01/2026"
END_DATE = "30/06/2026"

RAW_PATH.mkdir(parents=True, exist_ok=True)


catalog = pd.read_csv(CATALOG_PATH)

for _, row in catalog.iterrows():
    try:

        indicator_name = row["indicator"]
        series_id = row["series_id"]

        url = (
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}"
            f"/dados?formato=json"
            f"&dataInicial={START_DATE}"
            f"&dataFinal={END_DATE}"
        )

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if not data:
            print(f"[WARNING] {indicator_name}: nenhum registro retornado.")
            continue

        output_file = RAW_PATH / f"{indicator_name}.json"

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"[OK] {indicator_name}: {len(data)} registros salvos em {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {indicator_name}: {e}")