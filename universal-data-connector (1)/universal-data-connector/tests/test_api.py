from app.connectors.analytics_connector import AnalyticsConnector
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.services.business_rules import apply_voice_limits, paginate, prioritize_data
from app.services.data_identifier import identify_data_type
from app.services.voice_optimizer import summarize_for_voice


def test_connectors_load_data() -> None:
    assert len(CRMConnector().fetch()) > 0
    assert len(SupportConnector().fetch()) > 0
    assert len(AnalyticsConnector().fetch()) > 0


def test_voice_limit_and_pagination() -> None:
    crm_rows = prioritize_data(CRMConnector().fetch(status="active"))
    page_size = apply_voice_limits(limit=20, voice_mode=True)
    page = paginate(crm_rows, page=1, page_size=page_size)

    assert page_size == 10
    assert len(page) <= 10


def test_data_type_and_voice_summary() -> None:
    analytics_rows = AnalyticsConnector().fetch(metric="daily_active_users")
    data_type = identify_data_type(analytics_rows)
    summary_payload, context = summarize_for_voice(
        source="analytics",
        data=analytics_rows[:10],
        total_count=len(analytics_rows),
    )

    assert data_type.value == "time_series"
    assert "summary" in summary_payload[0]
    assert "voice" in context
