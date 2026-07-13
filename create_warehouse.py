from pathlib import Path
import duckdb

Path("data/warehouse").mkdir(parents=True, exist_ok=True)

duckdb.connect("data/warehouse/openmetrics.duckdb").close()