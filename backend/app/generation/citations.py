"""Parse the LLM output and build Citation objects from [Source N] references."""

from __future__ import annotations

import re

from app.schemas.query import Citation
from app.schemas.retrieval import RetrievedChunk

_SOURCE_REF = re.compile(r"\[source\s+(\d+)\]", re.IGNORECASE)
_LOW_CONF = re.compile(r"low[_\s]?confidence\s*:\s*(yes|no)", re.IGNORECASE)


def parse_llm_output(raw: str) -> tuple[str, bool]:
    """Return (answer_without_flag, low_confidence)."""
    low = False
    match = _LOW_CONF.search(raw)
    if match:
        low = match.group(1).lower() == "yes"
        raw = raw[: match.start()].rstrip()
    return raw.strip(), low


def referenced_indices(answer: str) -> list[int]:
    return sorted({int(n) for n in _SOURCE_REF.findall(answer)})


def build_citations(
    answer: str, chunks: list[RetrievedChunk], max_default: int = 4
) -> list[Citation]:
    """Cite the chunks the answer references; if none were referenced, cite the top few."""
    indices = referenced_indices(answer)
    chosen: list[RetrievedChunk] = []
    if indices:
        chosen = [chunks[n - 1] for n in indices if 1 <= n <= len(chunks)]
    if not chosen:
        chosen = chunks[:max_default]

    citations: list[Citation] = []
    seen: set[str] = set()
    for c in chosen:
        if c.chunk_id in seen:
            continue
        seen.add(c.chunk_id)
        citations.append(
            Citation(
                chunk_id=c.chunk_id,
                source_title=c.title,
                source_file=c.source_file,
                source_url=c.source_url,
                section_title=c.section_title,
                authority=c.authority,
                quote=c.text[:280].strip(),
            )
        )
    return citations
