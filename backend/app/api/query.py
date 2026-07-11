"""Query endpoints. Phase 4 adds the retrieval-only debug endpoint; Phase 5
adds the full grounded-answer endpoint.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.auth import get_current_user_id
from app.generation.answer import get_answer_generator
from app.retrieval.retriever import get_retriever
from app.schemas.query import QueryRequest, QueryResponse
from app.schemas.retrieval import RetrievedChunk

router = APIRouter(prefix="/api", tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest, user_id: str = Depends(get_current_user_id)) -> QueryResponse:
    return get_answer_generator().generate(request, user_id=user_id)


class QueryDebugRequest(BaseModel):
    question: str
    domain: str | None = None
    institution: str | None = None
    top_k: int = 8


class QueryDebugResponse(BaseModel):
    chunks: list[RetrievedChunk]
    count: int


@router.post("/query/debug", response_model=QueryDebugResponse)
def query_debug(req: QueryDebugRequest) -> QueryDebugResponse:
    chunks = get_retriever().retrieve(
        req.question, top_k=req.top_k, domain=req.domain, institution=req.institution
    )
    return QueryDebugResponse(chunks=chunks, count=len(chunks))
