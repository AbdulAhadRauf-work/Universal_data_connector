# Universal Data Connector

Production-ready FastAPI service that exposes a single, LLM-friendly interface to query CRM, support, and analytics data with voice-first optimizations.

## Features
- 3 connectors (`crm`, `support`, `analytics`) with a shared interface.
- Voice-aware limits and summarization (optimized for low-latency spoken responses).
- Data-type identification (`tabular`, `time_series`, etc.).
- Contextual metadata (`showing x of y`, freshness hints, pagination state).
- OpenAPI schema ready for LLM function/tool calling.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API
### Health
- `GET /health`

### Unified data endpoint
- `GET /data/{source}` where `source` is one of:
  - `crm`
  - `support`
  - `analytics`

Supported query parameters:
- `limit` (default `10`)
- `page` (default `1`)
- `voice_mode` (default `true`)
- `status` (CRM filter)
- `priority` (support filter)
- `customer_id` (support filter)
- `metric` (analytics filter)

## Example requests
```bash
curl 'http://127.0.0.1:8000/data/crm?status=active&voice_mode=true'
curl 'http://127.0.0.1:8000/data/support?priority=high&voice_mode=false&limit=5'
curl 'http://127.0.0.1:8000/data/analytics?metric=daily_active_users&voice_mode=true'
```

## Tests
```bash
pytest -q
```

## Docker
```bash
docker compose up --build
```
