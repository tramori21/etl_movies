from __future__ import annotations

from typing import Any, Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticsearchLoader:
    def __init__(self, es: Elasticsearch, index_name: str):
        self.es = es
        self.index_name = index_name

    def load(self, docs: Iterable[dict[str, Any]]) -> int:
        actions = []
        for doc in docs:
            actions.append(
                {
                    "_op_type": "index",
                    "_index": self.index_name,
                    "_id": doc["id"],
                    "_source": doc,
                }
            )

        if not actions:
            return 0

        success, _ = bulk(self.es, actions)
        return int(success)
