from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DataSource(str, Enum):
    crm = "crm"
    support = "support"
    analytics = "analytics"


class DataType(str, Enum):
    empty = "empty"
    tabular = "tabular"
    time_series = "time_series"
    hierarchical = "hierarchical"
    unknown = "unknown"


class Metadata(BaseModel):
    source: DataSource
    data_type: DataType
    total_results: int
    returned_results: int
    page: int
    page_size: int
    has_more: bool
    context: str
    freshness: str


class DataResponse(BaseModel):
    data: list[dict[str, Any]]
    metadata: Metadata


class ErrorResponse(BaseModel):
    detail: str = Field(..., examples=["Unsupported source requested"])
