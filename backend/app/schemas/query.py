"""Request/response schemas for the main /api/query endpoint."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.retrieval import RetrievedChunk


class QueryRequest(BaseModel):
    question: str
    # Defaults to banking (the MVP domain) so unspecified queries do RBI-first retrieval.
    domain: str | None = "banking_payments"
    institution: str | None = None
    top_k: int = 8
    include_debug: bool = False


class Citation(BaseModel):
    chunk_id: str
    source_title: str
    source_file: str
    source_url: str = ""
    section_title: str = ""
    authority: str = ""
    quote: str  # first ~280 chars of the cited chunk


class QueryResponse(BaseModel):
    answer: str
    category: str = "pending"
    category_label: str = ""
    risk_level: str = "pending"
    escalation_route: list[str] = Field(default_factory=list)
    evidence_checklist: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    is_unsupported: bool = False
    low_confidence: bool = False
    disclaimer: str = ""
    retrieved_chunks: list[RetrievedChunk] | None = None
    model_name: str = ""
    latency_ms: int = 0
    audit_id: str | None = None  # populated in Phase 7
