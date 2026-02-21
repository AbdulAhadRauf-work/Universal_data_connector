from typing import Any


def summarize_for_voice(source: str, data: list[dict[str, Any]], total_count: int) -> tuple[list[dict[str, Any]], str]:
    if not data:
        return data, "No matching records found."

    if source == "analytics":
        values = [item.get("value", 0) for item in data if isinstance(item.get("value"), (int, float))]
        avg_value = round(sum(values) / len(values), 2) if values else 0
        return (
            [{"summary": f"Showing {len(data)} of {total_count} metrics. Average value is {avg_value}."}],
            f"Showing aggregated metrics for voice ({len(data)} of {total_count}).",
        )

    return data, f"Showing {len(data)} of {total_count} most relevant records for voice."
