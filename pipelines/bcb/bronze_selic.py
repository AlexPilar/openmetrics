import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")
BRONZE_PATH = Path("data/bronze")
REQUIRED_COLUMNS = {"data", "valor"}

BRONZE_PATH.mkdir(parents=True, exist_ok=True)


for json_file in RAW_PATH.glob("*.json"):
    try:
        data = pd.read_json(json_file)

        if data.empty:
            print(f"[WARNING] {json_file.name}: arquivo vazio.")
            continue


        if not REQUIRED_COLUMNS.issubset(data.columns):
            print(f"[WARNING] {json_file.name}: colunas esperadas não encontradas.")
            continue
        
        data["data"] = pd.to_datetime(
            data["data"], 
            format="%d/%m/%Y"
            )
        
        data["valor"] = data["valor"].astype(float)

        
        output_file = BRONZE_PATH / f"{json_file.stem}.parquet"

        data.to_parquet(
            output_file,
            engine="pyarrow",
            compression="snappy",
            index=False
        )  

        print(
            f"[OK] {json_file.name}: "
            f"{len(data)} registros salvos em {output_file}"
        )

    except Exception as e:
        print(f"[ERROR] {json_file.name}: {e}")
