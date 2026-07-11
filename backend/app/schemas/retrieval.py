"""RetrievedChunk — a chunk returned from vector search, enriched with the
citation fields the UI and answer generator need.
"""

from __future__ import annotations

from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    chunk_id: str
    source_id: str
    text: str
    score: float  # cosine similarity, 0..1
    section_title: str = ""
    source_file: str = ""
    source_url: str = ""
    title: str = ""
    authority: str = ""
    institution: str = ""
    domain: str = ""
