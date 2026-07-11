from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.audit import AuditEntry
from app.storage import audit_repo

client = TestClient(app)


def test_insert_get_roundtrip_and_json_list():
    entry = AuditEntry(
        question="credit card 30 day rule",
        category="credit_card_grievance",
        risk_level="medium",
        answer_preview="preview",
        citation_count=2,
        source_ids_used=["src_a", "src_b"],
        model_name="extractive-none",
        latency_ms=7,
    )
    audit_repo.insert_audit(entry)
    got = audit_repo.get_audit(entry.audit_id)
    assert got is not None
    assert got.category == "credit_card_grievance"
    # JSON list column round-trips as a real list, not a string.
    assert got.source_ids_used == ["src_a", "src_b"]


def test_list_is_newest_first():
    old = AuditEntry(question="OLDER", timestamp=datetime(2020, 1, 1))
    new = AuditEntry(question="NEWER", timestamp=datetime(2035, 1, 1))
    audit_repo.insert_audit(old)
    audit_repo.insert_audit(new)
    rows = audit_repo.list_audits(limit=500)
    order = {r.question: i for i, r in enumerate(rows)}
    assert order["NEWER"] < order["OLDER"]


def test_api_list_and_404():
    assert client.get("/api/audit?limit=5").status_code == 200
    assert client.get("/api/audit/nonexistent-id").status_code == 404


def test_query_creates_audit_row_with_id():
    before = audit_repo.count_audits()
    resp = client.post("/api/query", json={"question": "credit card complaint not resolved in 30 days"})
    assert resp.status_code == 200
    assert resp.json()["audit_id"]
    assert audit_repo.count_audits() == before + 1
