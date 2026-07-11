from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.exceptions import InsufficientContext, SourceNotFound, register_exception_handlers


def _app() -> TestClient:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/nf")
    def nf():
        raise SourceNotFound("missing src")

    @app.get("/bad")
    def bad():
        raise InsufficientContext("no context")

    return TestClient(app)


def test_source_not_found_maps_to_404():
    r = _app().get("/nf")
    assert r.status_code == 404
    assert r.json() == {"error": "SourceNotFound", "detail": "missing src"}


def test_domain_error_maps_to_400():
    r = _app().get("/bad")
    assert r.status_code == 400
    assert r.json()["error"] == "InsufficientContext"
