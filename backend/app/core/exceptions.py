"""Custom exceptions + global handlers that return structured JSON errors."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class FinTrustError(Exception):
    """Base class for domain errors."""


class SourceNotFound(FinTrustError):
    """A requested source_id does not exist."""


class InsufficientContext(FinTrustError):
    """Retrieval returned nothing usable for grounding."""


class ClassifierError(FinTrustError):
    """The classifier could not process the input."""


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(SourceNotFound)
    async def _source_not_found(_request: Request, exc: SourceNotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"error": "SourceNotFound", "detail": str(exc)})

    @app.exception_handler(FinTrustError)
    async def _domain_error(_request: Request, exc: FinTrustError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": type(exc).__name__, "detail": str(exc)},
        )
