"""Reranking hook.

Phase 4 ships an identity reranker (preserves vector-similarity order). This is
the seam where a cross-encoder reranker (e.g. `cross-encoder/ms-marco-MiniLM-L-6-v2`)
can be dropped in later to reorder by true query-chunk relevance — usually the
single highest-ROI retrieval-quality upgrade after basic RAG works.
"""

from __future__ import annotations

from app.schemas.retrieval import RetrievedChunk


def rerank(chunks: list[RetrievedChunk], query: str) -> list[RetrievedChunk]:
    # TODO(reranker): score (query, chunk.text) pairs with a cross-encoder and
    # sort by that score. Keep the signature identical so it's a drop-in.
    return chunks
