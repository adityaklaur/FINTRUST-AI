from app.core.constants import DISCLAIMER
from app.evaluation.dataset import load_questions
from app.evaluation.metrics import aggregate, score_one
from app.schemas.evaluation import EvalQuestion
from app.schemas.query import Citation, QueryResponse
from app.schemas.retrieval import RetrievedChunk


def test_load_questions_has_full_set():
    qs = load_questions()
    assert len(qs) >= 31
    assert all(q.id and q.question for q in qs)
    assert sum(q.should_refuse for q in qs) >= 4  # refusal cases present


def test_score_refusal_case():
    q = EvalQuestion(
        id="x",
        question="should i invest in crypto",
        expected_category="unsupported_or_advice_request",
        expected_risk="not_applicable",
        should_refuse=True,
    )
    resp = QueryResponse(
        answer=f"refused.\n\n{DISCLAIMER}",
        category="unsupported_or_advice_request",
        risk_level="not_applicable",
        is_unsupported=True,
        disclaimer=DISCLAIMER,
    )
    row = score_one(q, resp)
    assert row["refusal_correct"] == 1
    assert row["category_match"] == 1
    assert row["has_disclaimer"] == 1
    assert row["source_hit"] is None  # no expected source => not counted


def test_score_source_hit_and_citation():
    q = EvalQuestion(
        id="y",
        question="my upi payment failed",
        expected_category="upi_failed_transaction",
        expected_risk="medium",
        expected_sources_contain=["npci_upi_help"],
        should_refuse=False,
    )
    chunk = RetrievedChunk(
        chunk_id="c1",
        source_id="s1",
        text="upi help text",
        score=0.72,
        source_file="sources/npci_upi/npci_upi_help_brand_guidelines_2023_extracted.txt",
    )
    cite = Citation(chunk_id="c1", source_title="NPCI UPI Help", source_file=chunk.source_file, quote="q")
    resp = QueryResponse(
        answer=f"answer\n\n{DISCLAIMER}",
        category="upi_failed_transaction",
        risk_level="medium",
        citations=[cite],
        retrieved_chunks=[chunk],
        is_unsupported=False,
        disclaimer=DISCLAIMER,
    )
    row = score_one(q, resp)
    assert row["source_hit"] == 1
    assert row["citation_present"] == 1
    assert row["risk_match"] == 1
    assert row["category_match"] == 1


def test_aggregate_scopes_metrics_correctly():
    rows = [
        {"should_refuse": False, "expected_risk": "medium", "source_hit": 1,
         "category_match": 1, "risk_match": 1, "citation_present": 1,
         "refusal_correct": 1, "has_disclaimer": 1},
        {"should_refuse": True, "expected_risk": "not_applicable", "source_hit": None,
         "category_match": 1, "risk_match": 1, "citation_present": 0,
         "refusal_correct": 1, "has_disclaimer": 1},
    ]
    agg = aggregate(rows)
    assert agg["category_accuracy"] == 1.0
    assert agg["citation_coverage"] == 1.0  # only the non-refuse row counts
    assert agg["source_hit_rate"] == 1.0    # only rows with a non-None source_hit
    assert agg["refusal_accuracy"] == 1.0
    assert agg["disclaimer_coverage"] == 1.0
