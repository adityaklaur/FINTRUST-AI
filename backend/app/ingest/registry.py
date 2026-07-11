"""CLI: build/refresh the source registry.

    python -m app.ingest.registry
"""

from __future__ import annotations

from collections import Counter

from app.core.config import SOURCES_DIR, get_settings
from app.core.logging import configure_logging, get_logger
from app.ingest.discover import discover_sources
from app.storage.db import create_db_and_tables
from app.storage.source_repo import upsert_many

log = get_logger("registry")


def _print_table(title: str, counter: Counter) -> None:
    print(f"\n{title}")
    print("-" * 40)
    for key, count in counter.most_common():
        print(f"  {key:<28} {count:>5}")


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    create_db_and_tables()

    docs = discover_sources(SOURCES_DIR)
    new, updated = upsert_many(docs)

    print(f"\nScanned {len(docs)} source files from {SOURCES_DIR}")
    print(f"  new={new}  updated={updated}")
    _print_table("By domain", Counter(d.domain for d in docs))
    _print_table("By authority", Counter(d.authority for d in docs))
    _print_table("Bank-specific by institution",
                 Counter(d.institution for d in docs if d.is_bank_specific))
    print()


if __name__ == "__main__":
    main()
