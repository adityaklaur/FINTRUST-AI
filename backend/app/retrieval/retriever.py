"""Retriever: vector search + metadata filter + score conversion + rerank."""

from __future__ import annotations

from functools import lru_cache

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.retrieval.filters import build_chroma_filter
from app.retrieval.reranker import rerank
from app.retrieval.vector_store import VectorStore
from app.schemas.retrieval import RetrievedChunk

log = get_logger("retriever")


def score_from_distance(distance: float) -> float:
    """ChromaDB cosine distance (0..2) -> similarity (1..0), clamped."""
    return max(0.0, min(1.0, 1.0 - distance / 2.0))


class Retriever:
    def __init__(self, vector_store: VectorStore | None = None, config: Settings | None = None):
        self.config = config or get_settings()
        self.vs = vector_store or VectorStore(self.config)

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        domain: str | None = None,
        institution: str | None = None,
    ) -> list[RetrievedChunk]:
        top_k = top_k or self.config.retrieval_top_k
        where = build_chroma_filter(domain, institution)
        res = self.vs.query(query, n_results=top_k, where=where)

        ids = (res.get("ids") or [[]])[0]
        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]

        chunks: list[RetrievedChunk] = []
        for cid, doc, meta, dist in zip(ids, docs, metas, dists):
            score = score_from_distance(dist)
            if score < self.config.min_chunk_score:
                continue
            meta = meta or {}
            chunks.append(
                RetrievedChunk(
                    chunk_id=cid,
                    source_id=str(meta.get("source_id", "")),
                    text=doc or "",
                    score=score,
                    section_title=str(meta.get("section_title", "")),
                    source_file=str(meta.get("source_file", "")),
                    source_url=str(meta.get("source_url", "")),
                    title=str(meta.get("title", "")),
                    authority=str(meta.get("authority", "")),
                    institution=str(meta.get("institution", "")),
                    domain=str(meta.get("domain", "")),
                )
            )

        chunks.sort(key=lambda c: c.score, reverse=True)
        return rerank(chunks, query)


@lru_cache
def get_retriever() -> Retriever:
    """Process-wide singleton so the embedding model loads only once."""
    return Retriever()
