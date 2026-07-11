# Deployment Checklist (free-first, step-by-step)

The "why" behind these choices is in `docs/deployment_strategies.md`. This is the
**do-this** list. Target: frontend on **Vercel**, backend on **Render** (free),
`LLM_PROVIDER=none` first. Everything below is optional-key-safe.

## 0. Pre-flight (local)
```bash
cd backend && .venv/bin/python -m pytest && .venv/bin/ruff check app tests
cd ../frontend && npm run build
```
All green? Push to a GitHub repo (`.env` and `node_modules` are git-ignored).

## 1. Backend → Render
- Render → **New → Blueprint** → select the repo (it reads `render.yaml`).
- The build rebuilds the vector store from `sources/` (≈1–2 min; downloads the
  ONNX embedder once). Health check: `/api/health`.
- Set env vars in the dashboard (the `sync: false` ones):
  - `CORS_ORIGINS` = your Vercel URL (fill after step 2), e.g. `https://fintrust.vercel.app`
  - *(optional)* `LLM_PROVIDER=groq` + `LLM_API_KEY=<groq key>` for fluent answers
- Note your backend URL, e.g. `https://fintrust-backend.onrender.com`.

## 2. Frontend → Vercel
- Vercel → **Add New → Project** → import the repo → **Root Directory = `frontend`**
  (it reads `frontend/vercel.json`; framework auto-detects Vite).
- Env var: `VITE_API_URL = https://fintrust-backend.onrender.com` (your Render URL).
- Deploy → note the URL, e.g. `https://fintrust.vercel.app`.

## 3. Wire the two together
- Back in Render: set `CORS_ORIGINS` to the Vercel URL → redeploy backend.
- Open the Vercel URL → ask a question → confirm you get a cited answer.
  (First backend hit after idle may cold-start ~30s on the free tier.)

## 4. (Optional) Fluent AI answers
- Get a free key: Groq (console.groq.com) or Gemini (aistudio.google.com/apikey).
- Render env: `LLM_PROVIDER=groq`, `LLM_API_KEY=<key>` → redeploy.
- Falls back to offline extractive automatically if the key is missing/limited.

## 5. (Optional) Accounts + per-user history
- Create a Supabase project (free). Enable Email auth.
- **Supabase → Auth → URL Configuration → Redirect URLs:** add
  `http://localhost:5173` and your Vercel URL.
- **Backend (Render):** `SUPABASE_JWT_SECRET` = Supabase → Settings → API → JWT secret.
- **Frontend (Vercel):** `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` (Settings → API).
- Redeploy both. The header now shows real magic-link sign-in; audit history is
  scoped per user. Without these vars, the app stays in anonymous mode.

## 6. (Optional) Persistent audit history
Free hosts wipe the local SQLite on restart. For durable history:
- Supabase → Settings → Database → Connection string.
- Render env: `DATABASE_URL=postgresql+psycopg://postgres:<pwd>@db.<ref>.supabase.co:5432/postgres`
- Add `psycopg[binary]` to `backend/requirements.txt` (currently commented). Redeploy.

## Secrets rule
Never commit `.env`. All keys go in the host dashboard (Render/Vercel/Supabase).
Only `VITE_SUPABASE_ANON_KEY` is public-safe; the service-role key must never
reach the frontend.

## Do we need K8s / Jenkins / API Gateway / RDS?
No — see `docs/deployment_strategies.md`. One Render service + one Vercel site is
enough for real early users.
