from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID


def _uuid_to_str(value):
    if isinstance(value, UUID):
        return str(value)
    return value


def _normalize_people(items):
    """
    items: список dict {'id': UUID/str, 'name': str}
    приводим к [{'id': '...', 'name': '...'}], без None.
    """
    if not items:
        return []

    out = []
    for it in items:
        if not it:
            continue
        pid = _uuid_to_str(it.get("id"))
        name = it.get("name") or ""
        out.append({"id": str(pid), "name": name})
    return out


@dataclass(frozen=True)
class Transformer:
    def transform_movie(self, row: dict[str, Any]) -> dict[str, Any]:
        movie_id = _uuid_to_str(row["id"])

        doc = {
            "id": str(movie_id),
            "imdb_rating": row.get("rating"),
            "genres": row.get("genres") or [],
            "title": row.get("title") or "",
            "description": row.get("description") or "",

            "directors_names": row.get("directors_names") or [],
            "actors_names": row.get("actors_names") or [],
            "writers_names": row.get("writers_names") or [],

            "directors": _normalize_people(row.get("directors")),
            "actors": _normalize_people(row.get("actors")),
            "writers": _normalize_people(row.get("writers")),
        }

        return doc

def transform(rows):
    return [Transformer().transform_movie(r) for r in rows]
