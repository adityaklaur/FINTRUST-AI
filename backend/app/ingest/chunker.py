"""Heading-aware, overlap-preserving chunker.

Strategy:
  1. Split text into paragraphs; single-line heading-like paragraphs become
     the running ``section_title`` rather than their own chunk.
  2. Oversized paragraphs are split by sentence so we never cut mid-sentence.
  3. Paragraphs are greedily packed up to ``target`` tokens.
  4. Each new chunk is seeded with a sentence-aligned overlap tail of the
     previous chunk (context continuity across boundaries).
  5. Any sub-``min`` chunk is merged into the previous one.

Token counts are estimated (≈4 chars/token) — good enough for sizing and
avoids a heavyweight tokenizer dependency.
"""

from __future__ import annotations

import re

from app.core.config import get_settings
from app.schemas.chunk import ChunkDoc
from app.schemas.source import SourceDoc

_HEADING_NUM = re.compile(r"^\d+(\.\d+)*[.)]?\s+\S")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_PARA_SPLIT = re.compile(r"\n\s*\n")


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _is_heading(line: str) -> bool:
    s = line.strip()
    if not s or len(s) > 120:
        return False
    if s.startswith("#"):
        return True
    if _HEADING_NUM.match(s) and len(s.split()) <= 14:
        return True
    letters = [c for c in s if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.8 and len(s.split()) <= 12:
        return True
    return False


def _sentences(text: str) -> list[str]:
    return [p.strip() for p in _SENTENCE_SPLIT.split(text) if p.strip()]


def _overlap_tail(text: str, overlap_tokens: int) -> str:
    acc: list[str] = []
    total = 0
    for s in reversed(_sentences(text)):
        if acc and total + estimate_tokens(s) > overlap_tokens:
            break
        acc.insert(0, s)
        total += estimate_tokens(s)
    return " ".join(acc)


def _units(text: str, target: int, hard_max: int) -> list[tuple[str, str]]:
    """Return (section_title, body) units; oversize bodies are sentence-split."""
    units: list[tuple[str, str]] = []
    section = ""
    for block in _PARA_SPLIT.split(text):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        if len(lines) == 1 and _is_heading(lines[0]):
            section = lines[0].strip().lstrip("#").strip()
            continue
        if estimate_tokens(block) <= hard_max:
            units.append((section, block))
            continue
        cur: list[str] = []
        cur_tok = 0
        for sent in _sentences(block):
            st = estimate_tokens(sent)
            if cur and cur_tok + st > target:
                units.append((section, " ".join(cur)))
                cur, cur_tok = [sent], st
            else:
                cur.append(sent)
                cur_tok += st
        if cur:
            units.append((section, " ".join(cur)))
    return units


def _metadata(src: SourceDoc, section: str, index: int, tokens: int) -> dict:
    return {
        "source_id": src.source_id,
        "source_file": src.file_path,
        "source_url": src.source_url or "",
        "title": src.title,
        "domain": src.domain,
        "subdomain": src.subdomain,
        "authority": src.authority,
        "institution": src.institution,
        "is_authoritative": bool(src.is_authoritative),
        "is_bank_specific": bool(src.is_bank_specific),
        "is_insurance_only": bool(src.is_insurance_only),
        "effective_year": int(src.effective_year),
        "section_title": section or "",
        "chunk_index": index,
        "token_count": tokens,
    }


def chunk_text(text: str, source_meta: SourceDoc) -> list[ChunkDoc]:
    cfg = get_settings()
    target = cfg.chunk_target_tokens
    hard_max = cfg.chunk_hard_max_tokens
    overlap = cfg.chunk_overlap_tokens
    min_tokens = cfg.chunk_min_tokens

    units = _units(text, target, hard_max)

    # Greedy pack into chunks up to `target`, seeding overlap on each new chunk.
    packed: list[tuple[str, str]] = []
    cur_text = ""
    cur_section = ""
    for section, body in units:
        if cur_text and estimate_tokens(cur_text) + estimate_tokens(body) > target:
            packed.append((cur_section, cur_text))
            tail = _overlap_tail(cur_text, overlap)
            cur_text = f"{tail}\n\n{body}" if tail else body
            cur_section = section
        else:
            if not cur_text:
                cur_section = section
            cur_text = body if not cur_text else f"{cur_text}\n\n{body}"
    if cur_text:
        packed.append((cur_section, cur_text))

    # Merge sub-min chunks into the previous one.
    merged: list[tuple[str, str]] = []
    for section, body in packed:
        if merged and estimate_tokens(body) < min_tokens:
            psec, ptext = merged[-1]
            merged[-1] = (psec, f"{ptext}\n\n{body}")
        else:
            merged.append((section, body))

    chunks: list[ChunkDoc] = []
    for i, (section, body) in enumerate(merged):
        tokens = estimate_tokens(body)
        chunks.append(
            ChunkDoc(
                chunk_id=f"{source_meta.source_id}_{i:04d}",
                source_id=source_meta.source_id,
                text=body,
                token_count=tokens,
                section_title=section,
                chunk_index=i,
                metadata=_metadata(source_meta, section, i, tokens),
            )
        )
    return chunks
