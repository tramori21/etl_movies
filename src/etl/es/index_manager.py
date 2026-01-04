from __future__ import annotations

import json
from pathlib import Path

from elasticsearch import Elasticsearch


class IndexManager:
    def __init__(self, es: Elasticsearch, index_name: str, schema_path: str):
        self.es = es
        self.index_name = index_name
        self.schema_path = Path(schema_path)

    def ensure_index(self) -> None:
        if self.es.indices.exists(index=self.index_name):
            return

        body = json.loads(self.schema_path.read_text(encoding="utf-8"))
        self.es.indices.create(index=self.index_name, body=body)
