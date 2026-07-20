from pathlib import Path

import pandas as pd

from utils.logger import logger

RAW_PATH = Path("data/raw")
BRONZE_PATH = Path("data/bronze")

REQUIRED_COLUMNS = {"data", "valor"}

BRONZE_PATH.mkdir(parents=True, exist_ok=True)


def load_json(json_file: Path):
    try:
        df = pd.read_json(json_file)

        if df.empty:
            logger.warning(f"{json_file.name}: empty file.")
            return None

        if not REQUIRED_COLUMNS.issubset(df.columns):
            logger.warning(
                f"{json_file.name}: required columns not found."
            )
            return None

        df["indicator"] = json_file.stem

        df["data"] = pd.to_datetime(
            df["data"],
            format="%d/%m/%Y"
        )

        df["valor"] = df["valor"].astype(float)

        return df

    except Exception as e:
        logger.error(f"{json_file.name}: {e}")
        return None


def build_bronze_dataframe(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    bronze_data = pd.concat(dataframes, ignore_index=True)

    bronze_data = bronze_data.sort_values(
        by=["indicator", "data"]
    )

    bronze_data = bronze_data[
        [
            "indicator",
            "data",
            "valor",
        ]
    ]

    return bronze_data


def save_parquet(bronze_data: pd.DataFrame):
    output_file = BRONZE_PATH / "bronze_sgs.parquet"

    bronze_data.to_parquet(
        output_file,
        engine="pyarrow",
        compression="snappy",
        index=False,
    )

    logger.info(
        f"{len(bronze_data)} records saved to {output_file}"
    )


def main():
    logger.info("Starting Bronze layer creation...")

    dataframes = []

    for json_file in RAW_PATH.glob("*.json"):
        df = load_json(json_file)

        if df is None:
            continue

        dataframes.append(df)

    if not dataframes:
        logger.error("No valid JSON files found.")
        raise ValueError("No valid JSON files found.")

    bronze_data = build_bronze_dataframe(dataframes)

    save_parquet(bronze_data)

    logger.info("Bronze layer created successfully.")


if __name__ == "__main__":
    main()