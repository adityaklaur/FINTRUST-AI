"""Translate (domain, institution) into a ChromaDB `where` filter.

These rules are the safety core of the product: they stop the system from
mixing insurance rules into banking answers, or citing research blogs as if
they were regulation. ChromaDB requires a single top-level operator, so
multi-condition filters are wrapped in `$and`.
"""

from __future__ import annotations

_AUTHORITATIVE_BANKING = ["RBI", "NPCI", "DICGC"]


def build_chroma_filter(domain: str | None, institution: str | None) -> dict | None:
    # Insurance is a walled garden: only insurance chunks, nothing else.
    if domain == "insurance":
        return {"is_insurance_only": True}

    if domain == "banking_payments":
        if institution:
            # Regulator sources PLUS the named bank's own documents.
            return {
                "$or": [
                    {"authority": {"$in": _AUTHORITATIVE_BANKING}},
                    {"institution": institution},
                ]
            }
        # No bank named -> regulator sources only (RBI-first), never insurance.
        return {
            "$and": [
                {"authority": {"$in": _AUTHORITATIVE_BANKING}},
                {"is_insurance_only": False},
            ]
        }

    # domain unspecified -> exclude insurance-only and research/blog content.
    return {
        "$and": [
            {"is_insurance_only": False},
            {"authority": {"$ne": "RESEARCH"}},
        ]
    }
