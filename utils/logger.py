import logging
from pathlib import Path

LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename=f'{LOG_PATH}/openmetrics.log',
    filemode='a',
    encoding='utf-8'
)


logger = logging.getLogger(__name__)
