from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseConnector(ABC):
    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file

    @abstractmethod
    def fetch(self, **filters: Any) -> list[dict[str, Any]]:
        """Fetch data from the concrete data source."""
