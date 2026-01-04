from datetime import datetime
import sys
from pathlib import Path

from elasticsearch import Elasticsearch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.pg.extractor import PostgresExtractor  # noqa: E402
from src.etl.transformer import Transformer  # noqa: E402
from src.etl.es.loader import ElasticsearchLoader  # noqa: E402


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


extractor = PostgresExtractor(PG_DSN)
transformer = Transformer()

es = Elasticsearch(ES_URL)
loader = ElasticsearchLoader(es, INDEX)

rows = extractor.fetch_movies(datetime.min)
docs = [transformer.transform_movie(r) for r in rows]

loaded = loader.load(docs)
print("LOADED:", loaded)

print(es.get(index=INDEX, id="99999999-9999-9999-9999-999999999999"))
