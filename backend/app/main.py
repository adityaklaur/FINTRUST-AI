"""FastAPI application entrypoint.

Run with:  uvicorn app.main:app --reload --port 8000  (from the backend/ dir)

Routers are included lazily-by-import so that Phase 1 boots even before the
retrieval / generation modules exist. Later phases register their routers here.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import audit, evaluation, health, query, sources, updates
from app.core.config import get_settings
from app.core.constants import APP_NAME, APP_VERSION
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.storage.db import create_db_and_tables

settings = get_settings()
configure_logging(settings.log_level)
log = get_logger("fintrust")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.ensure_dirs()
    create_db_and_tables()
    log.info("%s v%s starting (env=%s, llm=%s)", APP_NAME, APP_VERSION, settings.app_env, settings.llm_provider)
    yield
    log.info("%s shutting down", APP_NAME)


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sources.router)
app.include_router(query.router)
app.include_router(audit.router)
app.include_router(evaluation.router)
app.include_router(updates.router)

register_exception_handlers(app)


@app.get("/")
def root() -> dict:
    return {"name": APP_NAME, "version": APP_VERSION, "docs": "/docs", "health": "/api/health"}
