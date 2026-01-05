from __future__ import annotations

from typing import Any


class State:
    """Хранит состояние ETL (например, время последней успешной загрузки)."""

    def __init__(self, storage):
        self._storage = storage

    def get(self, key: str) -> Any:
        return self._storage.retrieve_state(key)

    def set(self, key: str, value: Any) -> None:
        self._storage.save_state(key, value)
