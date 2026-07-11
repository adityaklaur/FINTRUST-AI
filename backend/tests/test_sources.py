from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.ingest.discover import discover_sources
from app.main import app
from app.storage.db import create_db_and_tables


def _make_corpus(root: Path) -> None:
    files = {
        "regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt": "rbi card rules",
        "regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_faq.txt": "ombudsman faq",
        "npci_upi/npci_upi_help_brand_guidelines_2023_extracted.txt": "upi help",
        "bank_documents/hdfc_credit_card_mitc_english_extracted.txt": "hdfc mitc",
        "insurance_irdai/irdai_health_insurance_master_circular_2024.txt": "irdai health",
        "regulatory_rbi/download_manifest.json": "{}",
        "research_references/ragas_paper_html.html": "<html></html>",
        "sources.md": "# registry",
    }
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def test_discover_infers_domain_and_authority(tmp_path: Path):
    _make_corpus(tmp_path)
    docs = {d.file_path: d for d in discover_sources(tmp_path)}

    rbi = docs["sources/regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt"]
    assert rbi.domain == "banking_payments"
    assert rbi.authority == "RBI"
    assert rbi.is_authoritative is True
    assert rbi.subdomain == "credit_card"
    assert rbi.effective_year == 2025


def test_discover_bank_specific(tmp_path: Path):
    _make_corpus(tmp_path)
    docs = {d.file_path: d for d in discover_sources(tmp_path)}
    hdfc = docs["sources/bank_documents/hdfc_credit_card_mitc_english_extracted.txt"]
    assert hdfc.is_bank_specific is True
    assert hdfc.institution == "hdfc"
    assert hdfc.authority == "BANK"


def test_discover_insurance(tmp_path: Path):
    _make_corpus(tmp_path)
    docs = {d.file_path: d for d in discover_sources(tmp_path)}
    ins = docs["sources/insurance_irdai/irdai_health_insurance_master_circular_2024.txt"]
    assert ins.domain == "insurance"
    assert ins.is_insurance_only is True
    assert ins.authority == "IRDAI"


def test_discover_skips_non_sources(tmp_path: Path):
    _make_corpus(tmp_path)
    paths = {d.file_path for d in discover_sources(tmp_path)}
    assert not any(p.endswith(".json") for p in paths)
    assert not any(p.endswith(".html") for p in paths)
    assert not any(p.endswith("sources.md") for p in paths)


@pytest.fixture(scope="module")
def client():
    create_db_and_tables()
    with TestClient(app) as c:
        c.post("/api/sources/scan")  # scans the real corpus into the test DB
        yield c


def test_api_scan_and_filter_rbi(client: TestClient):
    resp = client.get("/api/sources", params={"authority": "RBI"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert all(d["authority"] == "RBI" for d in data)


def test_api_filter_insurance(client: TestClient):
    resp = client.get("/api/sources", params={"domain": "insurance"})
    assert resp.status_code == 200
    assert all(d["is_insurance_only"] for d in resp.json())


def test_api_unknown_source_404(client: TestClient):
    assert client.get("/api/sources/deadbeef0000").status_code == 404
