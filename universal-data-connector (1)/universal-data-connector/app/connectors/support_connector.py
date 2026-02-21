import json
from pathlib import Path

from .base import BaseConnector


class SupportConnector(BaseConnector):
    def __init__(self) -> None:
        root = Path(__file__).resolve().parents[2]
        super().__init__(root / "data" / "support_tickets.json")

    def fetch(self, **filters: str | int) -> list[dict]:
        with self.data_file.open(encoding="utf-8") as file:
            rows = json.load(file)

        priority = filters.get("priority")
        customer_id = filters.get("customer_id")
        if priority:
            rows = [row for row in rows if row.get("priority") == priority]
        if customer_id is not None:
            rows = [row for row in rows if row.get("customer_id") == customer_id]
        return rows
