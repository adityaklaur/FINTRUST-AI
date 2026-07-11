"""Map a category (+ the question wording) to a risk level."""

from __future__ import annotations

from app.classifier.taxonomy import RISK_RULES, UPI_ESCALATION_WORDS


def get_risk_level(category: str, question: str) -> str:
    ql = question.lower()

    # UPI failures are medium by default, high once the user signals it's stuck.
    if category == "upi_failed_transaction":
        return "high" if any(w in ql for w in UPI_ESCALATION_WORDS) else "medium"

    for level in ("high", "medium", "low", "not_applicable"):
        if category in RISK_RULES.get(level, []):
            return level
    return "medium"
