"""Evaluation schemas: a golden question and an aggregate report."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvalQuestion(BaseModel):
    id: str
    question: str
    expected_category: str
    expected_risk: str | None = None
    expected_sources_contain: list[str] = Field(default_factory=list)
    should_refuse: bool = False
    notes: str = ""


class EvalReport(BaseModel):
    total: int
    category_accuracy: float
    risk_accuracy: float
    citation_coverage: float
    source_hit_rate: float
    refusal_accuracy: float
    disclaimer_coverage: float
    per_question: list[dict] = Field(default_factory=list)
    failed_questions: list[str] = Field(default_factory=list)
    generated_at: str = ""
    provider: str = ""
    model_name: str = ""
