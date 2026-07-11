"""Evaluation endpoints: run synchronously or fetch the last saved report."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.evaluation.runner import load_latest, run_evaluation
from app.schemas.evaluation import EvalReport

router = APIRouter(prefix="/api", tags=["evaluation"])


@router.post("/evaluation/run", response_model=EvalReport)
def run() -> EvalReport:
    return run_evaluation()


@router.get("/evaluation/latest", response_model=EvalReport)
def latest() -> EvalReport:
    report = load_latest()
    if report is None:
        raise HTTPException(status_code=404, detail="no evaluation report yet; run POST /api/evaluation/run")
    return report
