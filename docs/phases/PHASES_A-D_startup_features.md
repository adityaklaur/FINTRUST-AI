# Phases A–D — Startup Features ✅

Implemented on 2026-07-11 on top of the working MVP. App stays fully functional
offline / no-auth at every step. Backend: 76 tests pass. Frontend builds clean.

## A. Document refresh pipeline (staying current WITHOUT training)
- `app/ingest/refresh.py` — `parse_rss` / `diff_new` (pure, tested), `fetch_feed`,
  `check_updates()` (read-only), `refresh(auto_ingest, max_docs)` (download + embed).
- `app/api/updates.py` — `GET /api/updates/check`, `POST /api/updates/refresh`.
- `app/schemas/updates.py`; config `rbi_rss_url`. CLI: `python -m app.ingest.refresh`.
- **Verified live:** pulled 10 real RBI notifications (Jun–Jul 2026) from
  `notifications_rss.xml`; flagged all as new. Tests: `tests/test_refresh.py`.

## B. LLM failover
- `app/generation/llm_client.py` — `LLMClient` is now param-driven; new `LLMRouter`
  tries primary → fallback → (caller) extractive. Never hard-fails.
- Config: `LLM_FALLBACK_PROVIDER/API_KEY/MODEL`. Gemini default → `gemini-2.5-flash`.
- Tests: `tests/test_llm.py`.

## C. Auth + per-user history + Postgres
- `app/core/auth.py` — optional Supabase HS256 JWT verification; no secret ⇒ ANON
  (public mode unchanged). `verify_token` + `get_current_user_id` dependency.
- `audit_log.user_id` column (+ idempotent migration in `db.py`); `/api/query` and
  `/api/audit` resolve the caller and scope history per user.
- `DATABASE_URL` (Postgres) supported via `settings.db_url`; default SQLite.
- Frontend: `lib/supabase.ts`, `components/AuthButton.tsx` (magic-link, env-gated),
  axios bearer-token interceptor. Deps: PyJWT, @supabase/supabase-js.
- **Verified:** JWT `sub=alice` → user "alice"; alice/bob/anon see only their own
  rows; tampered token → anon. Tests: `tests/test_auth.py`.

## D. Deployment integration
- `render.yaml` (backend; rebuilds the vector store at build time),
  `frontend/vercel.json` (SPA), `docs/DEPLOYMENT_CHECKLIST.md` (step-by-step incl.
  Supabase redirect URLs, LLM keys, Postgres). `frontend/.env.example`.

## How to use
```bash
# staying current
cd backend && .venv/bin/python -m app.ingest.refresh            # detect new RBI docs
.venv/bin/python -m app.ingest.refresh --ingest                 # download + embed them

# fluent answers (optional): backend/.env
LLM_PROVIDER=groq
LLM_API_KEY=...
LLM_FALLBACK_PROVIDER=gemini
LLM_FALLBACK_API_KEY=...

# accounts (optional): set SUPABASE_JWT_SECRET (backend) + VITE_SUPABASE_* (frontend)
# deploy: see docs/DEPLOYMENT_CHECKLIST.md
```
