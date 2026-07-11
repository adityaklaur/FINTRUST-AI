# Running FinTrust AI (verified MVP)

This is the tested, non-Docker path. Backend and frontend run in two terminals.

## Prerequisites
- **Python 3.13** (`/opt/homebrew/bin/python3.13` on this machine)
- **Node 20+** (Node 24 present)
- No API keys required — the app runs offline in `LLM_PROVIDER=none` mode.

---

## 1. Backend (port 8000)

```bash
cd backend
python3.13 -m venv .venv                 # first time only
.venv/bin/pip install -r requirements.txt  # first time only

# The registry + vector store are already built and committed under data/.
# To rebuild from scratch (optional):
#   .venv/bin/python -m app.ingest.registry     # scan sources/ -> SQLite
#   .venv/bin/python -m app.ingest.pipeline     # ingest the 12 seed docs -> ChromaDB

.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

Check: <http://localhost:8000/api/health> and API docs at <http://localhost:8000/docs>.

## 2. Frontend (port 5173)

```bash
cd frontend
npm install        # uses public npm via .npmrc (NOT corporate CodeArtifact)
npm run dev
```

Open <http://localhost:5173>. The dev server proxies `/api` → `localhost:8000`.

> **npm note:** your global npm points at a private AWS CodeArtifact registry that
> needs an auth token; `frontend/.npmrc` overrides it to public npm so installs
> don't hang. If you *want* CodeArtifact, run `aws codeartifact login --tool npm …`
> and delete `frontend/.npmrc`.

---

## 3. Upgrade answers from "extractive" to an LLM (optional)

Answers work offline (templated from retrieved chunks). For fluent prose, add a key:

```bash
# backend/.env
LLM_PROVIDER=groq          # or gemini | openai | anthropic
LLM_API_KEY=your_key_here
# LLM_MODEL=                # optional; blank uses a sensible per-provider default
```

- **Groq** (free, fast): <https://console.groq.com>
- **Gemini** (free tier): <https://aistudio.google.com/apikey>

Restart uvicorn. If the key/SDK is missing or a call fails, it silently falls back
to extractive mode — the app never hard-fails on the LLM layer.

Install the provider SDK you chose (only one needed):
```bash
.venv/bin/pip install groq          # or: google-generativeai / openai / anthropic
```

---

## 4. Tests, lint, evaluation

```bash
cd backend
.venv/bin/python -m pytest              # 65+ tests
.venv/bin/ruff check app tests          # lint
.venv/bin/python -m app.evaluation.runner   # quality report -> data/eval/
```

## 5. One-command (Docker, convenience)

```bash
docker compose up --build
# backend :8000, frontend :5173
```
The non-Docker path above is the verified one; Docker is provided for convenience.
