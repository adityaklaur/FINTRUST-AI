# Phase 7 — Audit Logging ✅

**Goal:** every answered query is persisted; a history is queryable via the API.

## What was built
- `app/schemas/audit.py` — `AuditEntry` SQLModel table (`audit_log`), incl. a JSON
  column for `source_ids_used`.
- `app/storage/audit_repo.py` — `insert_audit`, `list_audits` (newest-first,
  optional category/risk filters), `get_audit`, `count_audits`.
- `app/api/audit.py` — `GET /api/audit`, `GET /api/audit/{id}`.
- `app/generation/answer.py` — `_finalize()` writes an audit row on **every**
  return path (advice-refusal, insufficient-evidence, success) and sets
  `QueryResponse.audit_id`. Audit failure never breaks the answer (wrapped).
- `app/storage/db.py` — registers the audit model so the table is created.

## How to test
```bash
cd backend && .venv/bin/python -m pytest tests/test_audit.py -v
```

## Acceptance criteria
- [x] Every `POST /api/query` creates a row (verified: `audit_id` returned, count +1)
- [x] `GET /api/audit` returns newest-first
- [x] `GET /api/audit/{unknown}` → 404
- [x] `source_ids_used` round-trips as a real JSON list
- [x] Logged fields: question, domain/institution, category, risk, unsupported,
      answer_preview, citation_count, source_ids_used, model_name, latency_ms, timestamp
