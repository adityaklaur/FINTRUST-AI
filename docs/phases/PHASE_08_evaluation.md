# Phase 8 — Evaluation Harness ✅

**Goal:** run a golden question set through the full pipeline and score quality.

## What was built
- `data/eval/questions_mvp.jsonl` — **32** questions across credit-card, UPI,
  unauthorized, ombudsman, failed-transaction-TAT, loan, and unsupported/advice.
  (KYC is swapped for loan because no KYC doc is ingested yet — see note below.)
- `app/schemas/evaluation.py` — `EvalQuestion`, `EvalReport`.
- `app/evaluation/dataset.py` — JSONL loader.
- `app/evaluation/metrics.py` — `score_one` + `aggregate` (scoping: citations only
  over non-refusals; source-hit only where an expected source is declared).
- `app/evaluation/runner.py` — `run_evaluation()` + CLI; writes
  `report_<ts>.json` and `report_latest.json`, prints a gated summary.
- `app/api/evaluation.py` — `POST /api/evaluation/run`, `GET /api/evaluation/latest`.

## How to run
```bash
cd backend && .venv/bin/python -m app.evaluation.runner
```

## Latest result (offline `none` provider, extractive answers)
| metric | value | gate |
|---|---|---|
| category_accuracy | 100.0% | ≥70% ✅ |
| risk_accuracy | 100.0% | — |
| citation_coverage | 100.0% | — |
| source_hit_rate | 92.6% | — |
| refusal_accuracy | 100.0% | =100% ✅ |
| disclaimer_coverage | 100.0% | =100% ✅ |

## Lesson captured
q12 initially failed: the question said *"without my consent"* but the classifier
keyword is the literal substring *"without consent"* — the "my" broke the match, so
it fell through to refusal. Keyword classifiers match **literal substrings**; eval
questions must exercise real keywords. Fixed the wording, not the code.

## Note
To enable KYC questions, ingest `rbi_kyc_direction_2016_updated_2025.txt` (already
in the corpus/registry) and add KYC rows to the JSONL.
