import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")
BRONZE_PATH = Path("data/bronze")
REQUIRED_COLUMNS = {"data", "valor"}

BRONZE_PATH.mkdir(parents=True, exist_ok=True)

dataframes = []

for json_file in RAW_PATH.glob("*.json"):
    try:
        df = pd.read_json(json_file)

        if df.empty:
            print(f"[WARNING] {json_file.name}: arquivo vazio.")
            continue


        if not REQUIRED_COLUMNS.issubset(df.columns):
            print(f"[WARNING] {json_file.name}: colunas esperadas não encontradas.")
            continue

        df["indicator"] = json_file.stem
        
        df["data"] = pd.to_datetime(
            df["data"], 
            format="%d/%m/%Y"
            )
        
        df["valor"] = df["valor"].astype(float)

        dataframes.append(df)

    except Exception as e:
        print(f"[ERROR] {json_file.name}: {e}")


output_file = BRONZE_PATH / f"bronze_sgs.parquet"

if not dataframes:
    raise ValueError(
        "Nenhum arquivo encontrado"
    )

bronze_data = pd.concat(dataframes, ignore_index=True)

bronze_data = bronze_data.sort_values(
    by = ["indicator", "data"]
)

bronze_data = bronze_data[[
    "indicator",
    "data",
    "valor"
]]


bronze_data.to_parquet(
    output_file,
    engine="pyarrow",
    compression="snappy",
    index=False
)  

print(
    f"{len(bronze_data)} registros salvos em {output_file}"
)
