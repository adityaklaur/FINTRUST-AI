# Phase 10 — Polish & Demo Prep ✅

## What was done
- `app/core/exceptions.py` — `FinTrustError` + `SourceNotFound` / `InsufficientContext`
  / `ClassifierError`, with global handlers returning structured JSON (registered in
  `main.py`). Tested in `tests/test_exceptions.py`.
- **LLM model defaults refreshed** (`generation/llm_client.py`): anthropic →
  `claude-haiku-4-5-20251001`, gemini → `gemini-2.0-flash`; comment stresses
  overriding via `LLM_MODEL` and checking the provider's models page.
- `requirements.txt` pinned to the verified Python 3.13 set (kept from prior session,
  incl. `onnxruntime`, `tokenizers`).
- `Dockerfile` (backend + frontend) + root `docker-compose.yml` (dev-mode, `/api`
  proxy via `VITE_PROXY_TARGET`).
- `data/eval/demo_questions.md` — 10 demo questions.
- `docs/RUNNING.md` — verified run guide; README updated to point to it.

## Verified
- [x] `pytest` → 65 passed; `ruff check app tests` → clean.
- [x] Backend HTTP surface live: health, sources (93 RBI), query (grounded + audit_id),
      refusal, audit log, evaluation report.
- [x] Frontend builds and runs; full stack works through the dev proxy.
- [~] `docker compose up` — files provided; not executed here (no Docker daemon in this
      environment). The non-Docker path in RUNNING.md is the verified one.

## Known warnings (harmless)
- Starlette 1.3 suggests `httpx2` for its TestClient. Tests pass; revisit when the
  Starlette/httpx2 story settles.
