import duckdb

conn = duckdb.connect("./data/warehouse/openmetrics.duckdb")

conn.execute(
    """
    CREATE SCHEMA IF NOT EXISTS bronze;

    CREATE OR REPLACE TABLE bronze.bronze_sgs AS
    SELECT * FROM
    read_parquet("./data/bronze/bronze_sgs.parquet")
    """
)

conn.close()
