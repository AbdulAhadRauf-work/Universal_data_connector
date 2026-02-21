from fastapi import FastAPI

from app.config import settings
from app.routers import data, health
from app.utils.logging import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Unified and voice-optimized API for CRM, support, and analytics connectors.",
)

app.include_router(health.router)
app.include_router(data.router)
