from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonFileStorage:
    """Хранилище состояния в JSON-файле."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def retrieve_state(self, key: str) -> Any:
        if not self.file_path.exists():
            return None

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get(key)

    def save_state(self, key: str, value: Any) -> None:
        if self.file_path.exists():
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        else:
            data = {}

        data[key] = value

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file)
