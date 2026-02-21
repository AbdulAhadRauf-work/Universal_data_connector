import json
from pathlib import Path

from .base import BaseConnector


class CRMConnector(BaseConnector):
    def __init__(self) -> None:
        root = Path(__file__).resolve().parents[2]
        super().__init__(root / "data" / "customers.json")

    def fetch(self, **filters: str) -> list[dict]:
        with self.data_file.open(encoding="utf-8") as file:
            rows = json.load(file)

        status = filters.get("status")
        if status:
            rows = [row for row in rows if row.get("status") == status]
        return rows
