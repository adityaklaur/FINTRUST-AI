"""Scoring for a single question and aggregation across the set.

Each metric is intentionally simple and explainable — this is a correctness
dashboard, not a leaderboard. `source_hit` is `None` (not counted) for questions
that declare no expected source, and citation coverage is measured only over
non-refusal questions (a refusal correctly has zero citations).
"""

from __future__ import annotations

from app.core.constants import DISCLAIMER
from app.schemas.evaluation import EvalQuestion
from app.schemas.query import QueryResponse


def score_one(q: EvalQuestion, resp: QueryResponse) -> dict:
    retrieved_files = [c.source_file for c in (resp.retrieved_chunks or [])]

    if q.expected_sources_contain:
        source_hit: int | None = int(
            any(exp in f for exp in q.expected_sources_contain for f in retrieved_files)
        )
    else:
        source_hit = None

    return {
        "id": q.id,
        "question": q.question,
        "expected_category": q.expected_category,
        "predicted_category": resp.category,
        "category_match": int(resp.category == q.expected_category),
        "expected_risk": q.expected_risk,
        "predicted_risk": resp.risk_level,
        "risk_match": int(q.expected_risk is not None and resp.risk_level == q.expected_risk),
        "citation_present": int(len(resp.citations) > 0),
        "source_hit": source_hit,
        "should_refuse": q.should_refuse,
        "is_unsupported": resp.is_unsupported,
        "refusal_correct": int(bool(q.should_refuse) == bool(resp.is_unsupported)),
        "has_disclaimer": int(DISCLAIMER in resp.answer),
        "latency_ms": resp.latency_ms,
    }


def _mean(rows: list[dict], key: str) -> float:
    vals = [r[key] for r in rows if r.get(key) is not None]
    return round(sum(vals) / len(vals), 3) if vals else 0.0


def aggregate(rows: list[dict]) -> dict:
    non_refuse = [r for r in rows if not r["should_refuse"]]
    with_risk = [r for r in rows if r["expected_risk"] is not None]
    with_source = [r for r in rows if r["source_hit"] is not None]
    return {
        "category_accuracy": _mean(rows, "category_match"),
        "risk_accuracy": _mean(with_risk, "risk_match"),
        "citation_coverage": _mean(non_refuse, "citation_present"),
        "source_hit_rate": _mean(with_source, "source_hit"),
        "refusal_accuracy": _mean(rows, "refusal_correct"),
        "disclaimer_coverage": _mean(rows, "has_disclaimer"),
    }
