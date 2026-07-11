"""Liveness endpoint. No dependencies on the DB or vector store on purpose —
this must answer even when everything else is still warming up.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.constants import APP_VERSION

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "version": APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
