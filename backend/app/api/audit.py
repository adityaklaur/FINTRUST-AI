"""Audit history endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import get_current_user_id
from app.schemas.audit import AuditEntry
from app.storage import audit_repo

router = APIRouter(prefix="/api", tags=["audit"])


@router.get("/audit", response_model=list[AuditEntry])
def list_audit(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    category: str | None = None,
    risk_level: str | None = None,
    user_id: str = Depends(get_current_user_id),
) -> list[AuditEntry]:
    return audit_repo.list_audits(
        limit=limit, offset=offset, category=category, risk_level=risk_level, user_id=user_id
    )


@router.get("/audit/{audit_id}", response_model=AuditEntry)
def get_audit(audit_id: str) -> AuditEntry:
    entry = audit_repo.get_audit(audit_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="audit entry not found")
    return entry
