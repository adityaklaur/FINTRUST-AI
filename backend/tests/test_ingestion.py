import pytest

from app.core.config import get_settings
from app.ingest.chunker import chunk_text, estimate_tokens
from app.ingest.loaders import load_file
from app.schemas.source import SourceDoc

CFG = get_settings()


def _meta() -> SourceDoc:
    return SourceDoc(
        source_id="testid",
        file_path="sources/test/x.txt",
        title="Test Doc",
        domain="banking_payments",
        subdomain="credit_card",
        authority="RBI",
        institution="general",
        is_authoritative=True,
    )


def test_long_text_splits_into_multiple_chunks():
    text = "\n\n".join(f"This is paragraph number {i} about banking rules. " * 12
                       for i in range(30))
    chunks = chunk_text(text, _meta())
    assert len(chunks) > 1
    # No chunk exceeds the hard max.
    assert all(c.token_count <= CFG.chunk_hard_max_tokens for c in chunks)
    # chunk_ids are stable and ordered.
    assert chunks[0].chunk_id == "testid_0000"
    assert chunks[1].chunk_id == "testid_0001"


def test_heading_becomes_section_title():
    text = "INTRODUCTION\n\n" + ("This clause explains the policy. " * 40)
    chunks = chunk_text(text, _meta())
    assert chunks[0].section_title == "INTRODUCTION"


def test_small_trailing_chunk_is_merged():
    big = "A sentence about card disputes. " * 200  # forces multiple chunks
    text = big + "\n\nEnd."
    chunks = chunk_text(text, _meta())
    assert len(chunks) > 1
    # The tiny "End." must have been merged, not left as a sub-min chunk.
    assert all(c.token_count >= CFG.chunk_min_tokens for c in chunks)


def test_metadata_carries_retrieval_fields():
    chunks = chunk_text("Some banking text. " * 50, _meta())
    meta = chunks[0].metadata
    for key in ("source_id", "domain", "authority", "institution", "is_authoritative"):
        assert key in meta
    assert meta["authority"] == "RBI"
    assert isinstance(meta["is_authoritative"], bool)


def test_estimate_tokens_monotonic():
    assert estimate_tokens("short") < estimate_tokens("a much longer piece of text here")


def test_load_real_pdf_extracts_text():
    pytest.importorskip("pdfplumber")
    from app.core.config import PROJECT_ROOT

    pdf = PROJECT_ROOT / "sources/npci_upi/npci_upi_help_brand_guidelines_2023.pdf"
    if not pdf.exists():
        pytest.skip("seed PDF not present")
    assert len(load_file(pdf)) > 100


def test_html_mislabeled_as_pdf_is_recovered():
    # This "pdf" is actually an HTML page; the sniffing loader must still read it.
    from app.core.config import PROJECT_ROOT

    f = PROJECT_ROOT / "sources/regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_pdf.pdf"
    if not f.exists():
        pytest.skip("seed file not present")
    assert len(load_file(f)) > 100
