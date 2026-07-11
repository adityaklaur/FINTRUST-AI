"""Ingestion pipeline: registry -> load -> clean -> chunk -> embed -> ChromaDB.

CLI:
    python -m app.ingest.pipeline           # ingest the 12-doc seed set
    python -m app.ingest.pipeline --reset   # wipe collection first
    python -m app.ingest.pipeline --all-banking   # ingest every banking source
"""

from __future__ import annotations

import sys
import time

from pydantic import BaseModel, Field

from app.core.config import PROJECT_ROOT, get_settings
from app.core.logging import configure_logging, get_logger
from app.ingest.chunker import chunk_text
from app.ingest.loaders import load_file
from app.retrieval.vector_store import VectorStore
from app.storage import source_repo

log = get_logger("ingest")

# The 12 high-signal seed documents (Phase 3 of the plan).
INITIAL_SOURCE_FILES = [
    "sources/regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt",
    "sources/regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_faq.txt",
    "sources/regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_pdf.pdf",
    "sources/regulatory_rbi/rbi_failed_transactions_tat_compensation_2019_clean_extract.txt",
    "sources/regulatory_rbi/rbi_unauthorized_electronic_banking_customer_liability_2017.txt",
    "sources/regulatory_rbi/rbi_online_dispute_resolution_digital_payments_2020_clean_extract.txt",
    "sources/regulatory_rbi/rbi_floating_rate_emi_reset_2023_clean_extract.txt",
    "sources/regulatory_rbi/rbi_kfs_loans_advances_2024_clean_extract.txt",
    "sources/npci_upi/npci_upi_help_brand_guidelines_2023_extracted.txt",
    "sources/bank_documents/hdfc_credit_card_mitc_english_extracted.txt",
    "sources/bank_documents/axis_grievance_redressal_policy_2026_extracted.txt",
    "sources/bank_documents/sbi_card_customer_grievance_policy_extracted.txt",
]


class IngestionReport(BaseModel):
    total_files: int = 0
    total_chunks: int = 0
    ingested_files: list[str] = Field(default_factory=list)
    skipped_files: list[str] = Field(default_factory=list)
    errors: list[dict] = Field(default_factory=list)
    duration_seconds: float = 0.0


def _resolve_targets(source_ids, file_paths, all_banking):
    sources = source_repo.list_sources(limit=100000)
    by_id = {s.source_id: s for s in sources}
    by_path = {s.file_path: s for s in sources}
    if source_ids:
        return [by_id[i] for i in source_ids if i in by_id]
    if file_paths:
        return [by_path[p] for p in file_paths if p in by_path]
    if all_banking:
        return [s for s in sources if s.domain == "banking_payments"]
    return [by_path[p] for p in INITIAL_SOURCE_FILES if p in by_path]


def run_ingestion(
    source_ids: list[str] | None = None,
    file_paths: list[str] | None = None,
    reset: bool = False,
    all_banking: bool = False,
) -> IngestionReport:
    get_settings()
    vs = VectorStore()
    if reset:
        vs.reset()

    targets = _resolve_targets(source_ids, file_paths, all_banking)
    report = IngestionReport(total_files=len(targets))
    start = time.perf_counter()

    for src in targets:
        full = PROJECT_ROOT / src.file_path
        try:
            if not full.exists():
                report.skipped_files.append(src.file_path)
                source_repo.update_ingestion_status(src.source_id, "skipped", "file missing")
                continue
            text = load_file(full)
            if not text.strip():
                report.skipped_files.append(src.file_path)
                source_repo.update_ingestion_status(src.source_id, "skipped", "empty after load")
                continue
            chunks = chunk_text(text, src)
            n = vs.upsert_chunks(chunks)
            report.total_chunks += n
            report.ingested_files.append(src.file_path)
            source_repo.update_ingestion_status(src.source_id, "ingested", f"{n} chunks")
            log.info("ingested %s -> %d chunks", src.file_path, n)
        except Exception as exc:  # noqa: BLE001
            report.errors.append({"file": src.file_path, "error": str(exc)})
            source_repo.update_ingestion_status(src.source_id, "error", str(exc)[:200])
            log.exception("failed to ingest %s", src.file_path)

    report.duration_seconds = round(time.perf_counter() - start, 2)
    return report


def main() -> None:
    configure_logging()
    from app.core.config import SOURCES_DIR
    from app.ingest.discover import discover_sources
    from app.storage.db import create_db_and_tables

    create_db_and_tables()
    source_repo.upsert_many(discover_sources(SOURCES_DIR))  # ensure registry exists

    report = run_ingestion(
        reset="--reset" in sys.argv,
        all_banking="--all-banking" in sys.argv,
    )
    print(report.model_dump_json(indent=2))
    print(f"\nCollection now holds {VectorStore().count()} chunks.")


if __name__ == "__main__":
    main()
