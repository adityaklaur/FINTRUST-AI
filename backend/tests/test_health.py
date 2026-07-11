from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"]
    assert "timestamp" in body


def test_root_ok():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["name"] == "FinTrust AI"
