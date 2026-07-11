"""Document refresh: detect newly published RBI notifications and (optionally)
re-ingest them into the vector store.

This is how FinTrust AI "stays current" — there is NO model training. New rules
become answerable the moment their text is chunked and embedded.

Pipeline:
    1. FETCH  RBI notifications RSS (machine-readable, no scraping)
    2. DIFF   feed items vs. what's already in the source registry
    3. (opt)  DOWNLOAD new items into sources/
    4. (opt)  INGEST  discover metadata -> chunk -> embed -> ChromaDB

CLI:
    python -m app.ingest.refresh            # detect only, print report
    python -m app.ingest.refresh --refresh  # download new items (no embed)
    python -m app.ingest.refresh --ingest   # download AND embed new items
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import httpx

from app.core.config import SOURCES_DIR, get_settings
from app.core.logging import configure_logging, get_logger
from app.schemas.updates import FeedItem, UpdateReport
from app.storage import source_repo

log = get_logger("refresh")

_SLUG_RE = re.compile(r"[^a-z0-9]+")


# --------------------------------------------------------------------------- #
# Pure helpers (unit-tested, no network)
# --------------------------------------------------------------------------- #
def parse_rss(xml_text: str) -> list[FeedItem]:
    """Parse an RSS 2.0 feed into FeedItems. Returns [] on malformed XML."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    items: list[FeedItem] = []
    for node in root.iter("item"):

        def _text(tag: str) -> str:
            el = node.find(tag)
            return (el.text or "").strip() if el is not None and el.text else ""

        link = _text("link")
        items.append(
            FeedItem(
                title=_text("title"),
                link=link,
                guid=_text("guid") or link,
                pub_date=_text("pubDate"),
            )
        )
    return items


def diff_new(feed_items: list[FeedItem], known_links: set[str]) -> list[FeedItem]:
    """Return feed items whose link/guid is not already known (deduped)."""
    known = {k.strip().rstrip("/") for k in known_links if k}
    out: list[FeedItem] = []
    seen: set[str] = set()
    for item in feed_items:
        key = (item.link or item.guid).strip().rstrip("/")
        if not key or key in known or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _slug(text: str) -> str:
    s = _SLUG_RE.sub("_", text.lower()).strip("_")
    return s[:80] or "rbi_notification"


# --------------------------------------------------------------------------- #
# Network + orchestration
# --------------------------------------------------------------------------- #
def fetch_feed(url: str | None = None) -> tuple[list[FeedItem], str]:
    cfg = get_settings()
    url = url or cfg.rbi_rss_url
    try:
        resp = httpx.get(
            url,
            timeout=cfg.refresh_timeout_seconds,
            headers={"User-Agent": cfg.refresh_user_agent},
            follow_redirects=True,
        )
        resp.raise_for_status()
        return parse_rss(resp.text), ""
    except Exception as exc:  # noqa: BLE001 - network failure must not crash the caller
        log.warning("RBI feed fetch failed: %s", exc)
        return [], str(exc)


def _known_links() -> set[str]:
    return {s.source_url for s in source_repo.list_sources(limit=100000) if s.source_url}


def check_updates(url: str | None = None) -> UpdateReport:
    """Read-only: what's on the feed that we don't already have?"""
    cfg = get_settings()
    items, error = fetch_feed(url)
    known = _known_links()
    new = diff_new(items, known)
    return UpdateReport(
        checked_at=datetime.now(timezone.utc).isoformat(),
        feed_url=url or cfg.rbi_rss_url,
        feed_total=len(items),
        known_count=len(known),
        new_count=len(new),
        new_items=new[:50],
        error=error,
    )


def _download(item: FeedItem, dest_dir: Path) -> Path | None:
    cfg = get_settings()
    try:
        resp = httpx.get(
            item.link,
            timeout=cfg.refresh_timeout_seconds,
            headers={"User-Agent": cfg.refresh_user_agent},
            follow_redirects=True,
        )
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        log.warning("download failed for %s: %s", item.link, exc)
        return None
    ctype = resp.headers.get("content-type", "").lower()
    ext = ".pdf" if ("pdf" in ctype or item.link.lower().endswith(".pdf")) else ".html"
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"rbi_feed_{_slug(item.title)}{ext}"
    path.write_bytes(resp.content)
    return path


def refresh(auto_ingest: bool = False, max_docs: int = 5, url: str | None = None) -> UpdateReport:
    """Detect new items, download up to max_docs, and optionally embed them.

    Conservative by design: nothing is embedded unless auto_ingest=True, and
    downloads are capped, so a scheduled run can be reviewed before ingestion.
    """
    report = check_updates(url)
    if report.error or not report.new_items:
        return report

    from app.ingest.discover import discover_sources
    from app.ingest.pipeline import run_ingestion

    dest = SOURCES_DIR / "regulatory_rbi"
    staged: list[str] = []
    for item in report.new_items[:max_docs]:
        path = _download(item, dest)
        if path is not None:
            staged.append(f"sources/{path.relative_to(SOURCES_DIR).as_posix()}")

    if not staged:
        return report

    # Re-scan so the new files get metadata + stable source_ids in the registry.
    docs = discover_sources(SOURCES_DIR)
    source_repo.upsert_many(docs)
    report.staged = staged

    if auto_ingest:
        by_path = {d.file_path: d for d in docs}
        source_ids = [by_path[p].source_id for p in staged if p in by_path]
        result = run_ingestion(source_ids=source_ids)
        report.ingested = result.ingested_files
        report.chunks_added = result.total_chunks
        log.info("refresh embedded %d new chunks", result.total_chunks)

    return report


def main() -> None:
    configure_logging()
    from app.storage.db import create_db_and_tables

    create_db_and_tables()
    do_ingest = "--ingest" in sys.argv
    do_download = do_ingest or "--refresh" in sys.argv
    report = refresh(auto_ingest=do_ingest) if do_download else check_updates()
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
