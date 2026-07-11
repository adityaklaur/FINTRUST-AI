import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.retrieval.filters import build_chroma_filter
from app.retrieval.retriever import Retriever, score_from_distance


# --- pure unit tests (no data / no model) ---
def test_filter_insurance_is_walled():
    assert build_chroma_filter("insurance", None) == {"is_insurance_only": True}


def test_filter_banking_with_institution_uses_or():
    f = build_chroma_filter("banking_payments", "hdfc")
    assert "$or" in f


def test_filter_banking_no_institution_uses_and():
    f = build_chroma_filter("banking_payments", None)
    assert "$and" in f


def test_filter_none_excludes_research():
    assert "RESEARCH" in str(build_chroma_filter(None, None))


def test_score_conversion_endpoints():
    assert score_from_distance(0.0) == 1.0
    assert score_from_distance(2.0) == 0.0
    assert abs(score_from_distance(1.0) - 0.5) < 1e-9


# --- integration tests (ingest a few seeds into the isolated test store) ---
@pytest.fixture(scope="module")
def retriever():
    from app.core.config import SOURCES_DIR
    from app.ingest.discover import discover_sources
    from app.ingest.pipeline import run_ingestion
    from app.storage import source_repo
    from app.storage.db import create_db_and_tables

    create_db_and_tables()
    source_repo.upsert_many(discover_sources(SOURCES_DIR))
    report = run_ingestion(
        file_paths=[
            "sources/regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt",
            "sources/npci_upi/npci_upi_help_brand_guidelines_2023_extracted.txt",
            "sources/bank_documents/hdfc_credit_card_mitc_english_extracted.txt",
        ],
        reset=True,
    )
    if report.total_chunks == 0:
        pytest.skip("no chunks ingested (embedding model unavailable)")
    return Retriever()


def test_banking_no_institution_is_regulator_only(retriever):
    chunks = retriever.retrieve(
        "credit card complaint not resolved in 30 days", domain="banking_payments"
    )
    assert len(chunks) > 0
    assert all(c.authority in {"RBI", "NPCI", "DICGC"} for c in chunks)
    assert chunks[0].score > 0.4


def test_institution_lets_bank_docs_through(retriever):
    chunks = retriever.retrieve(
        "hdfc credit card fees and charges", domain="banking_payments", institution="hdfc"
    )
    assert len(chunks) > 0
    assert all(c.authority in {"RBI", "NPCI", "DICGC"} or c.institution == "hdfc" for c in chunks)


def test_debug_endpoint_returns_chunks(retriever):
    with TestClient(app) as client:
        resp = client.post(
            "/api/query/debug",
            json={"question": "credit card complaint", "domain": "banking_payments", "top_k": 5},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] >= 1
    assert "authority" in body["chunks"][0]
