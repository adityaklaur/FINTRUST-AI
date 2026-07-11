"""Document-refresh endpoints (detect / refresh new RBI notifications)."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.ingest.refresh import check_updates, refresh
from app.schemas.updates import UpdateReport

router = APIRouter(prefix="/api", tags=["updates"])


@router.get("/updates/check", response_model=UpdateReport)
def updates_check() -> UpdateReport:
    """Read-only: RBI feed items not yet in our corpus."""
    return check_updates()


@router.post("/updates/refresh", response_model=UpdateReport)
def updates_refresh(
    ingest: bool = Query(False, description="also embed downloaded docs"),
    max_docs: int = Query(5, ge=1, le=20),
) -> UpdateReport:
    """Admin action: download (and optionally embed) new notifications.

    Network + potentially heavy; intended to be gated behind admin auth later.
    """
    return refresh(auto_ingest=ingest, max_docs=max_docs)
