from collections.abc import Mapping

from app.models.common import DataType


def identify_data_type(data: list[Mapping[str, object]]) -> DataType:
    if not data:
        return DataType.empty

    sample = data[0]
    if "date" in sample and "value" in sample:
        return DataType.time_series
    if any(key.endswith("_id") for key in sample) and "created_at" in sample:
        return DataType.tabular
    if any(isinstance(value, dict) for value in sample.values()):
        return DataType.hierarchical
    return DataType.unknown
