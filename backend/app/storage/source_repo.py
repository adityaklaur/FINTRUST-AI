"""Persistence helpers for SourceDoc rows."""

from __future__ import annotations

from sqlmodel import Session, select

from app.schemas.source import SourceDoc
from app.storage.db import engine

# Fields never overwritten by a re-scan (so re-running discovery doesn't reset
# ingestion progress that the pipeline recorded).
_PRESERVE_ON_UPSERT = {"ingestion_status"}


def upsert_many(docs: list[SourceDoc]) -> tuple[int, int]:
    """Insert new docs / update existing ones. Returns (new, updated)."""
    new = updated = 0
    # expire_on_commit=False so the caller can keep reading these objects'
    # attributes after we commit (avoids SQLAlchemy DetachedInstanceError).
    with Session(engine, expire_on_commit=False) as session:
        for doc in docs:
            existing = session.get(SourceDoc, doc.source_id)
            if existing is None:
                session.add(doc)
                new += 1
            else:
                for key, value in doc.model_dump().items():
                    if key in _PRESERVE_ON_UPSERT:
                        continue
                    setattr(existing, key, value)
                session.add(existing)
                updated += 1
        session.commit()
    return new, updated


def upsert_source(doc: SourceDoc) -> None:
    upsert_many([doc])


def get_source(source_id: str) -> SourceDoc | None:
    with Session(engine) as session:
        return session.get(SourceDoc, source_id)


def list_sources(
    domain: str | None = None,
    authority: str | None = None,
    institution: str | None = None,
    ingestion_status: str | None = None,
    limit: int = 1000,
) -> list[SourceDoc]:
    with Session(engine) as session:
        stmt = select(SourceDoc)
        if domain:
            stmt = stmt.where(SourceDoc.domain == domain)
        if authority:
            stmt = stmt.where(SourceDoc.authority == authority)
        if institution:
            stmt = stmt.where(SourceDoc.institution == institution)
        if ingestion_status:
            stmt = stmt.where(SourceDoc.ingestion_status == ingestion_status)
        return list(session.exec(stmt.order_by(SourceDoc.file_path).limit(limit)))


def update_ingestion_status(source_id: str, status: str, notes: str = "") -> None:
    with Session(engine) as session:
        doc = session.get(SourceDoc, source_id)
        if doc is None:
            return
        doc.ingestion_status = status
        if notes:
            doc.notes = notes
        session.add(doc)
        session.commit()
