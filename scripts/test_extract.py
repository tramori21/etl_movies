from datetime import datetime
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.pg.extractor import PostgresExtractor  # noqa: E402

dsn = (
    "dbname=movies_database "
    "user=app "
    "password=app "
    "host=postgres "
    "port=5432 "
    "connect_timeout=5"
)

extractor = PostgresExtractor(dsn)

try:
    rows = extractor.fetch_movies(datetime.min)
    for row in rows:
        print(row)
except Exception as e:
    print("ERROR:", repr(e))
    raise
