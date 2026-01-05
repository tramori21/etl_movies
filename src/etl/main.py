from time import sleep
from datetime import datetime, timezone

import psycopg
from elasticsearch import Elasticsearch

from etl.config import settings
from etl.state.json_file_storage import JsonFileStorage
from etl.state.state import State
from etl.pg.extractor import PostgresExtractor
from etl.es.loader import ElasticsearchLoader
from etl.transformer import transform


def wait_for_postgres(dsn: str) -> None:
    while True:
        try:
            with psycopg.connect(dsn):
                print("Postgres is ready", flush=True)
                return
        except psycopg.OperationalError:
            print("Waiting for Postgres...", flush=True)
            sleep(2)


def wait_for_elasticsearch(es: Elasticsearch) -> None:
    while True:
        try:
            if es.ping():
                print("Elasticsearch is ready", flush=True)
                return
        except Exception:
            pass
        print("Waiting for Elasticsearch...", flush=True)
        sleep(2)


def main() -> None:
    print("ETL started", flush=True)

    wait_for_postgres(settings.pg_dsn)

    es = Elasticsearch(settings.es_host)
    wait_for_elasticsearch(es)

    storage = JsonFileStorage(settings.state_path)
    state = State(storage)

    extractor = PostgresExtractor(settings.pg_dsn)
    loader = ElasticsearchLoader(es, settings.index_name)

    while True:
        last = state.get(settings.state_key)
        last_dt = datetime.fromisoformat(last) if last else datetime.min.replace(tzinfo=timezone.utc)

        rows = extractor.fetch_movies(last_dt)

        if rows:
            docs = transform(rows)
            loader.load(docs)

            max_modified = max(r["modified"] for r in rows)
            if max_modified.tzinfo is None:
                max_modified = max_modified.replace(tzinfo=timezone.utc)

            state.set(settings.state_key, max_modified.isoformat())
            print(f"Loaded {len(rows)} movies", flush=True)
        else:
            print("No new movies", flush=True)

        sleep(10)


if __name__ == "__main__":
    main()
