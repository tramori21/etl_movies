import json
from pathlib import Path
from typing import Any


class State:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._state: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.file_path.exists():
            self._state = json.loads(self.file_path.read_text(encoding="utf-8"))

    def get(self, key: str, default=None):
        return self._state.get(key, default)

    def set(self, key: str, value) -> None:
        self._state[key] = value
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(
            json.dumps(self._state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
