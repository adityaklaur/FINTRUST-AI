"""Keyword + priority classifier.

Deterministic and fast. When an LLM is configured it could refine this, but the
keyword classifier is the always-available floor and what the tests pin.
"""

from __future__ import annotations

from app.classifier.taxonomy import CATEGORIES, CATEGORY_PRIORITY, STRONG_ADVICE


class Classifier:
    def classify(self, question: str) -> tuple[str, float]:
        ql = question.lower()

        # Advice/investment requests are refused regardless of other matches.
        if any(term in ql for term in STRONG_ADVICE):
            return ("unsupported_or_advice_request", 1.0)

        scores = {
            cat: sum(1 for kw in kws if kw in ql)
            for cat, kws in CATEGORIES.items()
            if cat != "unsupported_or_advice_request"
        }

        # Highest keyword count wins; ties break toward higher priority (earlier).
        best: str | None = None
        best_score = 0
        for cat in CATEGORY_PRIORITY:
            if scores.get(cat, 0) > best_score:
                best_score = scores[cat]
                best = cat

        if best is None or best_score == 0:
            return ("unsupported_or_advice_request", 0.0)

        confidence = round(best_score / max(1, len(ql.split())), 3)
        return (best, confidence)
