"""Look up the escalation route and evidence checklist for a category."""

from __future__ import annotations

from app.classifier.taxonomy import ESCALATION_ROUTES, EVIDENCE_CHECKLISTS

_DEFAULT_ESCALATION = [
    "Step 1: Contact the institution's customer care and note your reference number.",
    "Step 2: Escalate to its Grievance Redressal / Nodal Officer if unresolved.",
    "Step 3: Approach the relevant Ombudsman (RBI or Insurance) if still unresolved.",
]
_DEFAULT_EVIDENCE = [
    "Your complaint reference number",
    "Relevant dates and amounts",
    "Copies of any communication with the institution",
]


def get_escalation(category: str) -> list[str]:
    # Known categories (incl. unsupported -> []) return their stored value;
    # only a truly-unknown category falls back to the generic route.
    return ESCALATION_ROUTES.get(category, _DEFAULT_ESCALATION)


def get_evidence(category: str) -> list[str]:
    return EVIDENCE_CHECKLISTS.get(category, _DEFAULT_EVIDENCE)
