"""Source registry endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.core.config import SOURCES_DIR
from app.ingest.discover import discover_sources
from app.schemas.source import SourceDoc
from app.storage import source_repo

router = APIRouter(prefix="/api", tags=["sources"])


class IngestRequest(BaseModel):
    source_ids: list[str] | None = None
    file_paths: list[str] | None = None
    reset: bool = False


@router.get("/sources", response_model=list[SourceDoc])
def get_sources(
    domain: str | None = Query(default=None),
    authority: str | None = Query(default=None),
    institution: str | None = Query(default=None),
    ingestion_status: str | None = Query(default=None),
    limit: int = Query(default=1000, le=5000),
) -> list[SourceDoc]:
    return source_repo.list_sources(
        domain=domain,
        authority=authority,
        institution=institution,
        ingestion_status=ingestion_status,
        limit=limit,
    )


@router.get("/sources/{source_id}", response_model=SourceDoc)
def get_source(source_id: str) -> SourceDoc:
    doc = source_repo.get_source(source_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"source {source_id} not found")
    return doc


@router.post("/sources/scan")
def scan_sources() -> dict:
    docs = discover_sources(SOURCES_DIR)
    new, updated = source_repo.upsert_many(docs)
    return {"scanned": len(docs), "new": new, "updated": updated}


@router.post("/ingest")
def ingest(req: IngestRequest | None = None):
    # Imported lazily so the API module loads even before ChromaDB is installed.
    from app.ingest.pipeline import run_ingestion

    req = req or IngestRequest()
    return run_ingestion(
        source_ids=req.source_ids, file_paths=req.file_paths, reset=req.reset
    )
