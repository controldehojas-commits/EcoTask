from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStorage:
    """JSON-backed persistence layer for task records."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def load(self) -> list[dict[str, Any]]:
        try:
            raw = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw or "[]")
            if isinstance(data, list):
                return data
        except (OSError, json.JSONDecodeError):
            pass
        return []

    def save(self, records: list[dict[str, Any]]) -> None:
        self.file_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
