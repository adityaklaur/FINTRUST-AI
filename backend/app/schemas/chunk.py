"""ChunkDoc — one retrievable unit of text plus the metadata it inherits from
its parent SourceDoc. The ``metadata`` dict is what gets stored alongside the
vector in ChromaDB and drives retrieval filtering.
"""

from __future__ import annotations

from pydantic import BaseModel


class ChunkDoc(BaseModel):
    chunk_id: str  # f"{source_id}_{chunk_index:04d}"
    source_id: str
    text: str
    token_count: int
    section_title: str = ""
    chunk_index: int
    metadata: dict  # flattened SourceDoc fields; values are str|int|bool only
