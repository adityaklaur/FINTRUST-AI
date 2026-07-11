"""Run the golden questions through the full pipeline and produce a report.

CLI:  python -m app.evaluation.runner
Writes data/eval/report_<timestamp>.json + data/eval/report_latest.json and
prints a summary table.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import DATA_DIR, get_settings
from app.evaluation.dataset import load_questions
from app.evaluation.metrics import aggregate, score_one
from app.generation.answer import get_answer_generator
from app.schemas.evaluation import EvalReport
from app.schemas.query import QueryRequest

_EVAL_DIR = DATA_DIR / "eval"
_LATEST = _EVAL_DIR / "report_latest.json"


def run_evaluation(
    questions_path: Path | str | None = None,
    output_path: Path | str | None = None,
) -> EvalReport:
    settings = get_settings()
    questions = load_questions(questions_path)
    generator = get_answer_generator()

    rows: list[dict] = []
    for q in questions:
        resp = generator.generate(QueryRequest(question=q.question, include_debug=True))
        rows.append(score_one(q, resp))

    agg = aggregate(rows)
    failed = [r["id"] for r in rows if not r["category_match"] or not r["refusal_correct"]]

    report = EvalReport(
        total=len(rows),
        per_question=rows,
        failed_questions=failed,
        generated_at=datetime.now(timezone.utc).isoformat(),
        provider=settings.llm_provider,
        model_name=(generator.llm.model_name or "extractive"),
        **agg,
    )

    _EVAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(output_path) if output_path else _EVAL_DIR / f"report_{stamp}.json"
    payload = json.dumps(report.model_dump(), indent=2, default=str)
    out.write_text(payload, encoding="utf-8")
    _LATEST.write_text(payload, encoding="utf-8")
    return report


def load_latest() -> EvalReport | None:
    if not _LATEST.exists():
        return None
    return EvalReport(**json.loads(_LATEST.read_text(encoding="utf-8")))


def _print_summary(report: EvalReport) -> None:
    line = "=" * 56
    print(line)
    print(f"FinTrust AI — Evaluation ({report.total} questions)")
    print(f"provider={report.provider} model={report.model_name}")
    print(line)
    metrics = [
        ("category_accuracy", report.category_accuracy, 0.70),
        ("risk_accuracy", report.risk_accuracy, None),
        ("citation_coverage", report.citation_coverage, None),
        ("source_hit_rate", report.source_hit_rate, None),
        ("refusal_accuracy", report.refusal_accuracy, 1.0),
        ("disclaimer_coverage", report.disclaimer_coverage, 1.0),
    ]
    for name, val, gate in metrics:
        flag = ""
        if gate is not None:
            flag = "  ✅" if val >= gate else f"  ❌ (target ≥ {gate:.0%})"
        print(f"  {name:22} {val:6.1%}{flag}")
    print(line)
    if report.failed_questions:
        print(f"failed question ids: {', '.join(report.failed_questions)}")
    else:
        print("no category/refusal failures 🎉")
    print(line)


def main() -> None:
    _print_summary(run_evaluation())


if __name__ == "__main__":
    main()
