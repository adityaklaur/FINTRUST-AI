"""AnswerGenerator: the orchestration that ties retrieval, classification, LLM
generation (or extractive fallback), citations, and safety framing together.
"""

from __future__ import annotations

import time
from functools import lru_cache

from app.classifier.classifier import Classifier
from app.classifier.escalation import get_escalation, get_evidence
from app.classifier.risk import get_risk_level
from app.classifier.taxonomy import CATEGORY_LABELS
from app.core.config import Settings, get_settings
from app.core.constants import DISCLAIMER
from app.core.logging import get_logger
from app.generation.citations import build_citations, parse_llm_output
from app.generation.llm_client import LLMRouter
from app.generation.prompts import (
    ANSWER_PROMPT_TEMPLATE,
    SYSTEM_PROMPT,
    build_context,
    extractive_answer,
)
from app.generation.refusal import unsupported_response
from app.retrieval.retriever import Retriever, get_retriever
from app.schemas.audit import AuditEntry
from app.schemas.query import QueryRequest, QueryResponse
from app.storage import audit_repo

log = get_logger("answer")


class AnswerGenerator:
    def __init__(self, retriever: Retriever | None = None, llm: LLMRouter | None = None, config: Settings | None = None):
        self.config = config or get_settings()
        self.retriever = retriever or get_retriever()
        self.llm = llm or LLMRouter(self.config)
        self.classifier = Classifier()

    def generate(self, request: QueryRequest, user_id: str = "anonymous") -> QueryResponse:
        start = time.perf_counter()
        category, _conf = self.classifier.classify(request.question)

        # 1. Advice/unsupported request -> refuse before retrieving anything.
        if category == "unsupported_or_advice_request":
            resp = unsupported_response(request.question, "advice")
            return self._finalize(resp, request, start, user_id=user_id)

        # 2. Retrieve grounded evidence.
        chunks = self.retriever.retrieve(
            request.question,
            top_k=request.top_k,
            domain=request.domain,
            institution=request.institution,
        )
        best_score = max((c.score for c in chunks), default=0.0)

        # 3. Not enough evidence -> refuse (but keep the classification for context).
        if not chunks or best_score < self.config.refusal_score:
            resp = unsupported_response(request.question, "insufficient")
            resp.category = category
            resp.category_label = CATEGORY_LABELS.get(category, "")
            resp.risk_level = get_risk_level(category, request.question)
            if request.include_debug:
                resp.retrieved_chunks = chunks
            return self._finalize(resp, request, start, chunks, user_id)

        # 4. Generate the prose answer (LLM if available, else extractive).
        if self.llm.available:
            raw = self.llm.complete(
                SYSTEM_PROMPT,
                ANSWER_PROMPT_TEMPLATE.format(
                    question=request.question, context_block=build_context(chunks)
                ),
            )
            answer, low_conf = parse_llm_output(raw)
            model_name = self.llm.model_name
        else:
            answer, low_conf, model_name = "", False, "extractive-none"

        # Fall back to extractive if the LLM produced nothing.
        if not answer.strip():
            answer = extractive_answer(request.question, chunks)
            low_conf = low_conf or False
            if model_name.startswith("extractive"):
                model_name = "extractive-none"
            else:
                model_name = "extractive-fallback"

        resp = QueryResponse(
            answer=f"{answer.strip()}\n\n{DISCLAIMER}",
            category=category,
            category_label=CATEGORY_LABELS.get(category, category),
            risk_level=get_risk_level(category, request.question),
            escalation_route=get_escalation(category),
            evidence_checklist=get_evidence(category),
            citations=build_citations(answer, chunks),
            is_unsupported=False,
            low_confidence=low_conf or best_score < 0.5,
            disclaimer=DISCLAIMER,
            model_name=model_name,
        )
        if request.include_debug:
            resp.retrieved_chunks = chunks
        return self._finalize(resp, request, start, chunks, user_id)

    def _finalize(
        self,
        resp: QueryResponse,
        request: QueryRequest,
        start: float,
        chunks: list | None = None,
        user_id: str = "anonymous",
    ) -> QueryResponse:
        resp.latency_ms = int((time.perf_counter() - start) * 1000)
        self._write_audit(resp, request, chunks, user_id)
        return resp

    @staticmethod
    def _write_audit(
        resp: QueryResponse, request: QueryRequest, chunks: list | None, user_id: str
    ) -> None:
        """Persist an audit row. Never let a logging failure break the answer."""
        try:
            source_ids: list[str] = []
            seen: set[str] = set()
            for chunk in chunks or []:
                if chunk.source_id not in seen:
                    seen.add(chunk.source_id)
                    source_ids.append(chunk.source_id)
            entry = AuditEntry(
                user_id=user_id,
                question=request.question,
                domain=request.domain,
                institution=request.institution,
                category=resp.category,
                risk_level=resp.risk_level,
                is_unsupported=resp.is_unsupported,
                answer_preview=resp.answer[:200],
                citation_count=len(resp.citations),
                source_ids_used=source_ids,
                model_name=resp.model_name,
                latency_ms=resp.latency_ms,
            )
            audit_repo.insert_audit(entry)
            resp.audit_id = entry.audit_id
        except Exception as exc:  # noqa: BLE001
            log.warning("audit logging failed (%s); continuing without audit.", exc)


@lru_cache
def get_answer_generator() -> AnswerGenerator:
    return AnswerGenerator()
