from fastapi import APIRouter, HTTPException, Query

from app.connectors.analytics_connector import AnalyticsConnector
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.models.common import DataResponse, DataSource, Metadata
from app.services.business_rules import (
    apply_voice_limits,
    freshness_label,
    paginate,
    prioritize_data,
)
from app.services.data_identifier import identify_data_type
from app.services.voice_optimizer import summarize_for_voice

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/{source}", response_model=DataResponse)
def get_data(
    source: DataSource,
    limit: int = Query(default=10, ge=1, le=100),
    page: int = Query(default=1, ge=1),
    voice_mode: bool = Query(default=True),
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    customer_id: int | None = Query(default=None),
    metric: str | None = Query(default=None),
) -> DataResponse:
    connector_map = {
        DataSource.crm: CRMConnector(),
        DataSource.support: SupportConnector(),
        DataSource.analytics: AnalyticsConnector(),
    }

    connector = connector_map.get(source)
    if not connector:
        raise HTTPException(status_code=404, detail="Unsupported source requested")

    raw_data = connector.fetch(
        status=status,
        priority=priority,
        customer_id=customer_id,
        metric=metric,
    )

    total_results = len(raw_data)
    prioritized = prioritize_data(raw_data)
    final_limit = apply_voice_limits(limit=limit, voice_mode=voice_mode)
    page_data = paginate(prioritized, page=page, page_size=final_limit)

    context = f"Showing {len(page_data)} of {total_results} result(s)."
    payload = page_data

    if voice_mode:
        payload, context = summarize_for_voice(source=source.value, data=page_data, total_count=total_results)

    metadata = Metadata(
        source=source,
        data_type=identify_data_type(raw_data),
        total_results=total_results,
        returned_results=len(payload),
        page=page,
        page_size=final_limit,
        has_more=(page * final_limit) < total_results,
        context=context,
        freshness=freshness_label(prioritized),
    )
    return DataResponse(data=payload, metadata=metadata)
