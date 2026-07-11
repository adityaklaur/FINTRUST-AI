import pytest

from app.generation.citations import build_citations, parse_llm_output
from app.generation.prompts import extractive_answer
from app.generation.refusal import unsupported_response
from app.schemas.query import QueryRequest
from app.schemas.retrieval import RetrievedChunk


def _chunk(i: int) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=f"c{i}",
        source_id=f"s{i}",
        text=f"Clause {i}: complaints must be acknowledged and resolved. More detail here.",
        score=0.8,
        title=f"Doc {i}",
        authority="RBI",
        source_file=f"sources/x{i}.txt",
    )


# --- pure unit tests ---
def test_parse_llm_output_extracts_low_confidence():
    answer, low = parse_llm_output("The source states X [Source 1].\nLOW_CONFIDENCE: yes")
    assert "LOW_CONFIDENCE" not in answer
    assert low is True


def test_build_citations_maps_source_refs():
    chunks = [_chunk(1), _chunk(2), _chunk(3)]
    cites = build_citations("Per [Source 1] and [Source 3], ...", chunks)
    assert {c.chunk_id for c in cites} == {"c1", "c3"}


def test_build_citations_defaults_when_no_refs():
    chunks = [_chunk(1), _chunk(2)]
    assert len(build_citations("no refs here", chunks)) == 2


def test_extractive_answer_has_source_markers():
    text = extractive_answer("q", [_chunk(1), _chunk(2)])
    assert "[Source 1]" in text and "[Source 2]" in text


def test_refusal_helpers():
    advice = unsupported_response("should i invest", "advice")
    assert advice.is_unsupported and advice.category == "unsupported_or_advice_request"
    assert advice.disclaimer
    assert unsupported_response("q", "insufficient").is_unsupported


# --- integration: generate() over the isolated test store ---
class FakeLLM:
    available = True
    model_name = "fake-model"

    def complete(self, system: str, user: str) -> str:
        return "According to the source, complaints are acknowledged [Source 1].\nLOW_CONFIDENCE: no"


@pytest.fixture(scope="module")
def ingested():
    from app.ingest.discover import discover_sources
    from app.ingest.pipeline import run_ingestion
    from app.core.config import SOURCES_DIR
    from app.storage import source_repo
    from app.storage.db import create_db_and_tables

    create_db_and_tables()
    source_repo.upsert_many(discover_sources(SOURCES_DIR))
    report = run_ingestion(
        file_paths=[
            "sources/regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt",
            "sources/regulatory_rbi/rbi_unauthorized_electronic_banking_customer_liability_2017.txt",
        ],
        reset=True,
    )
    if report.total_chunks == 0:
        pytest.skip("no chunks ingested (embedding model unavailable)")


def test_generate_advice_is_refused(ingested):
    from app.generation.answer import AnswerGenerator

    resp = AnswerGenerator().generate(QueryRequest(question="should i invest in crypto"))
    assert resp.is_unsupported is True
    assert resp.category == "unsupported_or_advice_request"


def test_generate_grounded_extractive(ingested):
    from app.generation.answer import AnswerGenerator

    resp = AnswerGenerator().generate(
        QueryRequest(question="what happens if a credit card complaint is not resolved in 30 days")
    )
    assert resp.is_unsupported is False
    assert resp.disclaimer and resp.disclaimer in resp.answer
    assert len(resp.escalation_route) >= 2
    assert len(resp.citations) >= 1
    assert resp.category == "credit_card_grievance"
    assert resp.risk_level == "medium"


def test_generate_with_mock_llm(ingested):
    from app.generation.answer import AnswerGenerator

    resp = AnswerGenerator(llm=FakeLLM()).generate(
        QueryRequest(question="unauthorized transaction on my card")
    )
    assert "[Source 1]" in resp.answer
    assert resp.model_name == "fake-model"
    assert resp.risk_level == "high"  # unauthorized_transaction
