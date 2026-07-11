"""Schemas for the document-refresh pipeline (staying current without training)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FeedItem(BaseModel):
    title: str = ""
    link: str = ""
    guid: str = ""
    pub_date: str = ""


class UpdateReport(BaseModel):
    checked_at: str = ""
    feed_url: str = ""
    feed_total: int = 0  # items currently on the feed
    known_count: int = 0  # feed links already in our registry
    new_count: int = 0  # feed items not yet in our corpus
    new_items: list[FeedItem] = Field(default_factory=list)
    error: str = ""
    # populated only when refresh(auto_ingest=...) actually downloads/ingests
    staged: list[str] = Field(default_factory=list)
    ingested: list[str] = Field(default_factory=list)
    chunks_added: int = 0
