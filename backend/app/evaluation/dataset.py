"""Load the golden evaluation questions from JSONL."""

from __future__ import annotations

import json
from pathlib import Path

from app.core.config import DATA_DIR
from app.schemas.evaluation import EvalQuestion

DEFAULT_QUESTIONS_PATH = DATA_DIR / "eval" / "questions_mvp.jsonl"


def load_questions(path: Path | str | None = None) -> list[EvalQuestion]:
    p = Path(path) if path else DEFAULT_QUESTIONS_PATH
    questions: list[EvalQuestion] = []
    with p.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            questions.append(EvalQuestion(**json.loads(line)))
    return questions
