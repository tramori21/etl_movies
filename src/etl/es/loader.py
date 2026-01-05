from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticsearchLoader:
    def __init__(self, es: Elasticsearch, index_name: str):
        self.es = es
        self.index_name = index_name

        # ВАЖНО: создаём индекс со схемой, иначе ES сделает динамический маппинг,
        # и упадут nested-запросы и агрегации в тестах.
        if not self.es.indices.exists(index=self.index_name):
            schema_path = os.getenv("ES_SCHEMA_PATH", "src/etl/es/es_schema.json")
            schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))

            create_kwargs: dict[str, Any] = {}
            if isinstance(schema, dict):
                if "settings" in schema:
                    create_kwargs["settings"] = schema["settings"]
                if "mappings" in schema:
                    create_kwargs["mappings"] = schema["mappings"]

            self.es.indices.create(index=self.index_name, **create_kwargs)

    def load(self, docs: Iterable[dict[str, Any]]) -> int:
        actions = [
            {
                "_op_type": "index",
                "_index": self.index_name,
                "_id": doc["id"],
                "_source": doc,
            }
            for doc in docs
        ]

        if not actions:
            return 0

        success, _ = bulk(self.es, actions)
        return int(success)
