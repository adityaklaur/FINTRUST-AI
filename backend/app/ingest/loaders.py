"""File loaders + text cleaning.

Content is dispatched by *sniffing magic bytes*, not by file extension — the
corpus contains HTML error pages saved with a `.pdf` extension (RBI blocked
direct downloads), and trusting the extension would silently drop them.

Cleaning is intentionally conservative: we fix mojibake and drop standalone
page-number lines, but we NEVER touch clause numbers or bullet markers because
those are load-bearing in regulatory text ("as per clause 5.2 ...").
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import ftfy

_PAGE_NUMBER_LINE = re.compile(r"^\s*\d{1,4}\s*$")
_TAG = re.compile(r"<[^>]+>")
_SCRIPT_STYLE = re.compile(r"(?is)<(script|style|head)[^>]*>.*?</\1>")
_MANY_BLANKS = re.compile(r"\n\s*\n\s*\n+")


def _clean(text: str) -> str:
    text = ftfy.fix_text(text)
    kept = [ln for ln in text.split("\n") if not _PAGE_NUMBER_LINE.match(ln)]
    text = "\n".join(kept)
    text = _MANY_BLANKS.sub("\n\n", text)
    return text.strip()


def _sniff(path: Path) -> str:
    with open(path, "rb") as fh:
        head = fh.read(1024)
    if head[:5] == b"%PDF-":
        return "pdf"
    low = head.lstrip().lower()
    if low.startswith((b"<!doc", b"<html", b"<?xml")) or b"<html" in low[:300]:
        return "html"
    return "text"


def load_text(path: Path) -> str:
    return _clean(path.read_text(encoding="utf-8", errors="ignore"))


def load_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    raw = _SCRIPT_STYLE.sub(" ", raw)
    return _clean(html.unescape(_TAG.sub(" ", raw)))


def load_pdf(path: Path) -> str:
    """Extract text with pdfplumber; fall back to pypdf if that yields nothing."""
    text = ""
    try:
        import pdfplumber

        with pdfplumber.open(str(path)) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages)
    except Exception:
        text = ""

    if not text.strip():
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(path))
            text = "\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception:
            text = ""

    return _clean(text)


def load_file(path: Path) -> str:
    kind = _sniff(path)
    if kind == "pdf":
        return load_pdf(path)
    if kind == "html":
        return load_html(path)
    return load_text(path)
