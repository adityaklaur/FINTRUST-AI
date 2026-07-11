"""Persistence for audit_log rows. Mirrors source_repo conventions."""

from __future__ import annotations

from sqlalchemy import func
from sqlmodel import Session, select

from app.schemas.audit import AuditEntry
from app.storage.db import engine


def insert_audit(entry: AuditEntry) -> AuditEntry:
    # expire_on_commit=False so the caller can read entry.audit_id after commit.
    with Session(engine, expire_on_commit=False) as session:
        session.add(entry)
        session.commit()
    return entry


def list_audits(
    limit: int = 50,
    offset: int = 0,
    category: str | None = None,
    risk_level: str | None = None,
    user_id: str | None = None,
) -> list[AuditEntry]:
    with Session(engine) as session:
        stmt = select(AuditEntry)
        if user_id:
            stmt = stmt.where(AuditEntry.user_id == user_id)
        if category:
            stmt = stmt.where(AuditEntry.category == category)
        if risk_level:
            stmt = stmt.where(AuditEntry.risk_level == risk_level)
        stmt = stmt.order_by(AuditEntry.timestamp.desc()).offset(offset).limit(limit)
        return list(session.exec(stmt))


def get_audit(audit_id: str) -> AuditEntry | None:
    with Session(engine) as session:
        return session.get(AuditEntry, audit_id)


def count_audits() -> int:
    with Session(engine) as session:
        return int(session.exec(select(func.count()).select_from(AuditEntry)).one())
