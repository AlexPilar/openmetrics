import pandas as pd
from pathlib import Path
import json

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")
CATALOG_PATH = Path("metadata/bcb_sgs.json")

# REQUIRED_COLUMNS = {"data", "valor"}

SILVER_PATH.mkdir(parents=True, exist_ok=True)

with CATALOG_PATH.open("r", encoding="utf-8") as f:
    catalog = json.load(f)

dataframes = []

for parquet_file in BRONZE_PATH.glob("*.parquet"):
    try:
        data = pd.read_parquet(parquet_file)

        if data.empty:
            print(f"[WARNING] {parquet_file.name}: arquivo vazio.")
            continue
        
        indicator_name = parquet_file.stem
        indicator_metadata = catalog[indicator_name]
        

        data["indicator"] = indicator_name
        data["frequency"] = indicator_metadata["frequency"]
        data["source"] = indicator_metadata["source"]
        data["unit"] = indicator_metadata["unit"]

        dataframes.append(data)

    except Exception as e:
        print(f"[ERROR] {parquet_file.name}: {e}")

output_file = SILVER_PATH / f"sgs_silver.parquet"

if not dataframes:
    raise ValueError(
        "Nenhum dado encontrado para gerar a camada Silver."
    )

silver_data = pd.concat(dataframes, ignore_index=True)

silver_data = silver_data.rename(
    columns={
        "data": "date",
        "valor": "value"
    }
)

silver_data = silver_data.sort_values(
    ["indicator", "date"]
)

silver_data = silver_data[
    [
        "indicator",
        "date",
        "value",
        "frequency",
        "source",
        "unit"
    ]
]

silver_data.to_parquet(
    output_file,
    engine="pyarrow",
    compression="snappy",
    index=False
)  

print(
    f"[OK] Camada Silver Criada com"
    f"{len(silver_data)} registros salvos em {output_file}"
)
