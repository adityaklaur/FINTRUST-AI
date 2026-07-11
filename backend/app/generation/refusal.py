"""Refusal responses: advice requests and insufficient-evidence cases."""

from __future__ import annotations

from app.core.constants import DISCLAIMER
from app.schemas.query import QueryResponse

_ADVICE = (
    "I can't provide investment, legal, tax, or personalized financial advice. "
    "I can only explain what public regulatory and bank documents say, and outline "
    "the standard grievance / escalation process. For a decision, please consult a "
    "qualified professional or the official source directly."
)

_INSUFFICIENT = (
    "I couldn't find enough relevant source material to answer this confidently. "
    "Try rephrasing or adding details (the bank, product, or specific issue). "
    "I only answer from trusted public documents and won't guess."
)


def unsupported_response(question: str, reason: str = "insufficient") -> QueryResponse:
    is_advice = reason == "advice"
    body = _ADVICE if is_advice else _INSUFFICIENT
    return QueryResponse(
        answer=f"{body}\n\n{DISCLAIMER}",
        category="unsupported_or_advice_request" if is_advice else "pending",
        category_label="Unsupported / Advice Request" if is_advice else "",
        risk_level="not_applicable" if is_advice else "pending",
        is_unsupported=True,
        disclaimer=DISCLAIMER,
        model_name="refusal",
    )
