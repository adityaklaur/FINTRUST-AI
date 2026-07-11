"""The SourceDoc model — one row per source file in the corpus.

This is both the SQLModel table (persistence) and the API response shape.
Every ingested chunk inherits its metadata from its parent SourceDoc, so the
correctness of retrieval filtering starts here.
"""

from __future__ import annotations

from sqlmodel import Field, SQLModel


class SourceDoc(SQLModel, table=True):
    __tablename__ = "sources"

    source_id: str = Field(primary_key=True, index=True)  # sha256(file_path)[:12]
    file_path: str = Field(index=True)  # relative to project root, e.g. "sources/..."
    title: str = ""
    source_url: str = ""

    # domain: banking_payments | insurance | research_reference | dataset
    domain: str = Field(default="banking_payments", index=True)
    subdomain: str = "general"
    # authority: RBI | NPCI | BANK | IRDAI | DICGC | SACHET | INSURER | RESEARCH
    authority: str = Field(default="RBI", index=True)
    institution: str = Field(default="general", index=True)  # "general" if not entity-specific

    is_authoritative: bool = True
    is_bank_specific: bool = False
    is_insurance_only: bool = False
    effective_year: int = 0

    # pending | ingested | skipped | error
    ingestion_status: str = Field(default="pending", index=True)
    notes: str = ""
