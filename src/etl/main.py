from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone

import backoff
from elasticsearch import Elasticsearch

from src.etl.es.index_manager import IndexManager
from src.etl.es.loader import ElasticsearchLoader
from src.etl.pg.extractor import PostgresExtractor
from src.etl.state.state import State
from src.etl.transformer import Transformer

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("etl")

PG_DSN = (
    "dbname=movies_database "
    "user=app "
    "password=app "
    "host=postgres "
    "port=5432 "
    "connect_timeout=5"
)

ES_URL = "http://elasticsearch:9200"
INDEX = "movies"
SCHEMA_PATH = "src/etl/es/es_schema.json"

STATE_PATH = "data/state.json"
STATE_KEY = "last_modified"

POLL_SECONDS = int(os.getenv("POLL_SECONDS", "10"))


@backoff.on_exception(backoff.expo, Exception, max_time=60)
def run_once(state: State) -> int:
    es = Elasticsearch(ES_URL)
    IndexManager(es, INDEX, SCHEMA_PATH).ensure_index()

    last = state.get(STATE_KEY)
    if last:
        last_dt = datetime.fromisoformat(last)
    else:
        last_dt = datetime.min.replace(tzinfo=timezone.utc)

    extractor = PostgresExtractor(PG_DSN)
    transformer = Transformer()

    rows = extractor.fetch_movies(last_dt)
    if not rows:
        return 0

    docs = [transformer.transform_movie(r) for r in rows]

    loader = ElasticsearchLoader(es, INDEX)
    loaded = loader.load(docs)

    max_updated = max(r["modified"] for r in rows)
    if max_updated.tzinfo is None:
        max_updated = max_updated.replace(tzinfo=timezone.utc)

    state.set(STATE_KEY, max_updated.isoformat())
    return loaded


def main():
    state = State(STATE_PATH)

    while True:
        loaded = run_once(state)
        logger.info("Loaded: %s", loaded)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
