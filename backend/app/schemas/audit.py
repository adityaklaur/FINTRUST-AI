"""AuditEntry — one row per answered query.

This is the compliance backbone: who asked what, how it was classified, which
sources were used, which model produced it, and how long it took. Persisted to
SQLite; also returned directly by the /api/audit endpoints.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def _utcnow_naive() -> datetime:
    # Store naive UTC so SQLite sorts correctly and JSON output is clean.
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _new_audit_id() -> str:
    return uuid.uuid4().hex[:16]


class AuditEntry(SQLModel, table=True):
    __tablename__ = "audit_log"

    audit_id: str = Field(default_factory=_new_audit_id, primary_key=True, index=True)
    timestamp: datetime = Field(default_factory=_utcnow_naive, index=True)
    user_id: str = Field(default="anonymous", index=True)  # Supabase 'sub', or "anonymous"

    question: str = ""
    domain: str | None = None
    institution: str | None = None

    category: str = "pending"
    risk_level: str = "pending"
    is_unsupported: bool = False

    answer_preview: str = ""  # first ~200 chars of the answer
    citation_count: int = 0
    # Stored as a JSON array column (list of source_ids that backed the answer).
    source_ids_used: list[str] = Field(default_factory=list, sa_column=Column(JSON))

    model_name: str = ""
    latency_ms: int = 0
