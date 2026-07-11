"""Corpus discovery: walk sources/ and infer metadata from folder + filename.

Filename conventions in this corpus are consistent enough that we can derive
domain / authority / institution / subdomain deterministically — no LLM needed.
This keeps the registry cheap, reproducible, and easy to audit.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from app.schemas.source import SourceDoc

# Files we never register as sources.
SKIP_SUFFIXES = {".html", ".json", ".md"}
SKIP_NAME_SUBSTRINGS = ("manifest",)

BANK_INSTITUTIONS = {
    "hdfc", "icici", "axis", "sbi", "kotak", "idfc", "bob", "canara",
    "federal", "hsbc", "pnb", "union", "yesbank", "rbl", "indusind", "au",
}

# Ordered: first keyword hit wins, so specific rules precede generic ones.
SUBDOMAIN_RULES: list[tuple[tuple[str, ...], str]] = [
    (("credit_card", "credit card", "credit_debit", "mitc"), "credit_card"),
    (("debit_card", "debit card"), "debit_card"),
    (("unauthorized", "unauthorised"), "unauthorized_transaction"),
    (("failed_transaction", "tat", "turn_around"), "failed_transaction"),
    (("chargeback",), "chargeback"),
    (("dispute", "udir", "odr"), "dispute_resolution"),
    (("ombudsman",), "ombudsman"),
    (("kyc", "aml", "cft"), "kyc"),
    (("upi", "bhim"), "upi"),
    (("deceased", "death_claim", "nominee", "legal_heir"), "deceased_claim"),
    (("cheque",), "cheque"),
    (("locker", "safe_deposit"), "locker"),
    (("grievance", "redressal"), "grievance"),
    (("emi", "kfs", "loan", "floating_rate", "advances"), "loan"),
    (("deposit",), "deposit_account"),
    (("health",), "insurance_health"),
    (("motor",), "insurance_motor"),
    (("life", "saral_jeevan"), "insurance_life"),
    (("griha", "property"), "insurance_property"),
]

_TITLE_STRIP = (
    "_clean_extract", "_extracted", "_second_snapshot", "_snapshot",
    "_document_page", "_english", "_text", "_p0", "_p1",
)


def _source_id(file_path: str) -> str:
    return hashlib.sha256(file_path.encode("utf-8")).hexdigest()[:12]


def _year_from(name: str) -> int:
    for y in re.findall(r"(?:19|20)\d{2}", name):
        if 1990 <= int(y) <= 2035:
            return int(y)
    return 0


def _title_from(stem: str) -> str:
    s = stem
    for suf in _TITLE_STRIP:
        s = s.replace(suf, "")
    s = s.replace("_", " ").strip()
    return (s[:1].upper() + s[1:]) if s else stem


def _subdomain_from(name: str) -> str:
    low = name.lower()
    for keys, sub in SUBDOMAIN_RULES:
        if any(k in low for k in keys):
            return sub
    return "general"


def _infer(rel: Path) -> SourceDoc | None:
    """Infer a SourceDoc from a path relative to the sources/ root, or None to skip."""
    name = rel.name
    low = name.lower()

    if rel.suffix.lower() in SKIP_SUFFIXES:
        return None
    if any(sub in low for sub in SKIP_NAME_SUBSTRINGS):
        return None
    if name == "sources.md":
        return None

    folder = rel.parts[0] if rel.parts else ""
    domain, authority, institution = "banking_payments", "RBI", "general"
    is_auth, is_bank, is_ins = True, False, False

    if folder == "regulatory_rbi":
        if low.startswith("dicgc"):
            authority = "DICGC"
        elif low.startswith("sachet"):
            authority = "SACHET"
        else:
            authority = "RBI"
    elif folder == "npci_upi":
        authority = "NPCI"
    elif folder == "bank_documents":
        authority, is_bank, is_auth = "BANK", True, False
        prefix = rel.stem.split("_")[0]
        if prefix == "standard":
            institution = "standard_chartered"
        elif prefix in BANK_INSTITUTIONS:
            institution = prefix
        else:
            institution = prefix or "general"
    elif folder == "insurance_irdai":
        domain, is_ins = "insurance", True
        if "irdai" in low or low.startswith("insurance_ombudsman"):
            authority, is_auth = "IRDAI", True
        else:
            authority, is_auth = "INSURER", False
    elif folder == "research_references":
        domain, authority, is_auth = "research_reference", "RESEARCH", False
    elif folder == "datasets":
        domain, authority, is_auth = "dataset", "RESEARCH", False
    else:
        domain, authority, is_auth = "research_reference", "RESEARCH", False

    file_path = f"sources/{rel.as_posix()}"
    return SourceDoc(
        source_id=_source_id(file_path),
        file_path=file_path,
        title=_title_from(rel.stem),
        source_url="",
        domain=domain,
        subdomain=_subdomain_from(name),
        authority=authority,
        institution=institution,
        is_authoritative=is_auth,
        is_bank_specific=is_bank,
        is_insurance_only=is_ins,
        effective_year=_year_from(name),
        ingestion_status="pending",
        notes="",
    )


def discover_sources(sources_root: Path) -> list[SourceDoc]:
    """Return one SourceDoc per registrable file under ``sources_root``."""
    docs: list[SourceDoc] = []
    for path in sorted(sources_root.rglob("*")):
        if not path.is_file():
            continue
        doc = _infer(path.relative_to(sources_root))
        if doc is not None:
            docs.append(doc)
    return docs
