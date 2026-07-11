# FinTrust AI — Claude Implementation Prompt Pack v2

This prompt pack is for Claude Opus/Max/High-context coding sessions. It is written for the **current existing FinTrust AI codebase**, not for a fresh scaffold.

Use one task per Claude chat. Do not paste all tasks into one session.

## Master Context Block

Paste this before every Claude task:

```text
You are a senior full-stack AI engineer working on FinTrust AI.

Project root:
FINTRUST-AI/

Read first:
- README.md
- docs/RUNNING.md
- docs/00_DECISIONS_AND_STACK.md
- docs/TECHNICAL_IMPLEMENTATION_PLAN.md
- sources/sources.md

Do NOT read, print, or expose secret values from:
- docs/API_LLM_API_SDK_KEYS.txt

Current project status:
- This is an existing working MVP, not a blank project.
- Backend: FastAPI, Pydantic, SQLModel/SQLite, ChromaDB.
- Frontend: React 18, TypeScript, Vite, Tailwind CSS.
- Retrieval: direct ChromaDB usage, not LangChain.
- Default answer mode: LLM_PROVIDER=none, extractive/cited answer generation.
- Optional LLM providers: Gemini, Groq, OpenAI, Anthropic.
- Tests and evaluation already exist.

Product:
FinTrust AI is a source-grounded financial-services copilot for banking, payments, grievance redressal, compliance, and claims-support workflows.

Hard safety rules:
1. Do not provide final legal, financial, tax, regulatory, credit, or claim-admissibility advice.
2. Do not answer from model memory when retrieved sources are missing.
3. Always preserve citations.
4. If source evidence is weak, return an insufficient-context/refusal answer.
5. Do not mix banking/payment retrieval with insurance retrieval unless insurance is selected.
6. Do not use research_reference or dataset files as authoritative answer sources.
7. If a bank is selected, retrieve RBI/NPCI/DICGC sources plus that bank's sources.
8. If no bank is selected, prefer RBI/NPCI/DICGC authoritative sources.

Engineering rules:
1. Inspect files before editing.
2. Make the smallest safe change that satisfies the task.
3. Preserve working behavior.
4. Add/update tests for changed logic.
5. Do not add heavy dependencies unless you explain why and ask first.
6. Do not introduce LangChain unless there is a concrete, justified need.
7. Keep LLM_PROVIDER=none working.
8. After changes, list files changed and exact commands to run.
```

## Task 0 — Current-State Audit

Use this before any major change.

```text
Task: Current-state audit only. Do not edit files.

Read:
- README.md
- docs/RUNNING.md
- docs/00_DECISIONS_AND_STACK.md
- docs/TECHNICAL_IMPLEMENTATION_PLAN.md
- sources/sources.md
- backend/requirements.txt
- frontend/package.json

Inspect:
- backend/app
- backend/tests
- frontend/src

Return:
1. What is already implemented.
2. What is partially implemented.
3. What is missing versus the technical plan.
4. Any documentation drift.
5. The next 5 highest-value implementation tasks.
6. Exact local commands to run.

Do not modify files.
```

## Task 1 — Documentation Drift Fix

```text
Task: Fix documentation drift only.

Goal:
Make README.md, docs/RUNNING.md, docs/00_DECISIONS_AND_STACK.md, docs/TECHNICAL_IMPLEMENTATION_PLAN.md, and docs/CLAUDE_IMPLEMENTATION_PROMPT.md consistent with the actual app.

Known truths:
- Frontend is React + TypeScript + Vite, not Streamlit.
- Claude prompt lives at docs/CLAUDE_IMPLEMENTATION_PROMPT.md.
- There is no top-level prompts/ folder.
- There is no top-level implementation_notes/ folder.
- The current MVP intentionally avoids LangChain.
- The current default is LLM_PROVIDER=none.
- Optional LLM providers must remain optional.

Do not change application code.

Acceptance criteria:
- No docs say Streamlit is the current frontend.
- No docs point to prompts/CLAUDE_IMPLEMENTATION_PROMPT.md.
- No docs say LangChain is required for MVP.
- Running instructions are still accurate.
```

## Task 2 — Retrieval Quality Improvement

```text
Task: Improve retrieval quality without changing public API response shape.

Read:
- backend/app/retrieval/
- backend/app/ingest/
- backend/app/schemas/
- sources/sources.md

Improve:
1. Metadata filters:
   - banking queries must not retrieve insurance chunks
   - insurance queries must retrieve only insurance chunks
   - user-facing answers must not retrieve research_reference or dataset chunks
   - selected bank queries must retrieve RBI/NPCI/DICGC + selected bank
2. Authority ranking:
   - RBI/NPCI/DICGC > selected bank > other bank > insurance > research
3. Source diversity:
   - avoid returning all top chunks from the same source when other relevant sources exist
4. Debug output:
   - retrieved chunks should include source title, authority, institution, score, section

Acceptance criteria:
- Existing tests pass.
- Add tests for insurance exclusion.
- Add tests for selected bank filter.
- Add tests that research_reference is excluded.
- Run at least these queries manually:
  1. credit card complaint not resolved in 30 days
  2. UPI payment failed money deducted
  3. unauthorized debit from account
  4. bank increased EMI and tenure
  5. deceased depositor claim
```

## Task 3 — Answer Quality And Citation Discipline

```text
Task: Improve answer quality and citation reliability.

Read:
- backend/app/generation/answer.py
- backend/app/generation/citations.py
- backend/app/generation/llm_client.py
- backend/app/classifier/
- backend/tests/

Every answer must include:
1. direct answer
2. source-grounded explanation
3. evidence/documents checklist
4. escalation route
5. caveat/refusal if source context is weak
6. citation block
7. disclaimer

Rules:
- Do not say "you are entitled" without source wording.
- Do not invent deadlines.
- Do not mention unrelated banks.
- If retrieval score is weak, refuse with helpful next steps.

Acceptance criteria:
- Unsupported/advice queries are refused.
- Supported answers include citations.
- Citation quote and source file are visible in API response.
- Existing generation tests pass.
```

## Task 4 — Classifier Expansion

```text
Task: Expand classifier categories and tests.

Read:
- backend/app/classifier/
- sources/sources.md classifier sections

Add or verify categories:
- loan_penal_charges
- floating_rate_emi_reset
- deposit_account_service_charge
- cheque_collection_delay
- deceased_depositor_claim
- safe_deposit_locker
- bbps_bill_payment_dispute
- nach_autopay_mandate_dispute
- unclaimed_deposit_udgam
- dicgc_deposit_insurance
- insurance_health_claim
- insurance_motor_claim
- insurance_grievance

Acceptance criteria:
- At least 40 classifier tests.
- Every category has risk level.
- Every category has escalation route.
- Existing query API still returns category and risk.
```

## Task 5 — Evaluation Dataset Upgrade

```text
Task: Upgrade evaluation dataset and reporting.

Read:
- backend/data/eval/questions_mvp.jsonl
- backend/app/evaluation/
- sources/sources.md

Goal:
Expand evaluation to at least 80 questions.

Must cover:
- credit card grievance
- UPI failed transaction
- unauthorized transaction
- KYC
- Ombudsman
- failed transaction TAT
- floating EMI reset
- loan penal charges/KFS
- deceased depositor claim
- cheque collection delay
- unsupported/advice request

Report must include:
- category accuracy
- risk accuracy
- source hit rate
- citation coverage
- refusal accuracy
- top failed questions
- category confusion matrix

Acceptance criteria:
- Evaluation runner completes.
- Report saved under backend/data/eval/.
- README/RUNNING explains eval command.
```

## Task 6 — React UI Polish

```text
Task: Improve React frontend UX without changing backend API contracts.

Read:
- frontend/src
- README.md
- docs/RUNNING.md

Improve:
1. Query page layout.
2. Category and risk badges.
3. Citation cards.
4. Retrieved chunk expanders.
5. Audit history table.
6. Source explorer filters.
7. Empty/loading/error states.
8. Responsive layout.

Design rules:
- Professional and minimal.
- Citations visible by default.
- Disclaimer always visible with answer.
- Risk level obvious.
- No gimmicks.

Acceptance criteria:
- npm run build passes.
- No console errors.
- Query path works with backend running.
```

## Task 7 — Optional LLM Provider Hardening

```text
Task: Harden optional LLM provider support.

Read:
- backend/app/generation/llm_client.py
- backend/.env.example
- docs/RUNNING.md

Do not expose API keys.

Goals:
- Keep LLM_PROVIDER=none as default.
- If provider SDK/key is missing, app should fall back to extractive mode.
- Add clear logs, not user-facing crashes.
- Support LLM_MODEL env override.
- Document provider setup safely.

Acceptance criteria:
- App works with LLM_PROVIDER=none.
- App does not crash if provider key is missing.
- No API keys in tests/logs/docs.
```

## Task 8 — Free / Near-Free Deployment Readiness

```text
Task: Prepare FinTrust AI for free or near-free showcase deployment.

Read:
- docs/RUNNING.md
- docs/deployment_strategies.md
- docker-compose.yml
- backend/requirements.txt
- frontend/package.json
- backend/app/core/config.py
- frontend/.npmrc

Update/create:
- docs/DEPLOYMENT_CHECKLIST.md
- frontend/.env.example if missing
- backend/.env.example if deployment variables are missing
- render.yaml only if it clearly helps and does not break local Docker
- docs/FREE_DEPLOYMENT_QUICKSTART.md

Target deployment strategy:
- Frontend: Cloudflare Pages or Vercel Free
- Backend: Render Free first, Koyeb Free as alternative
- LLM: LLM_PROVIDER=none first, then optional Gemini/Groq free key
- Database/vector store: bundled/prebuilt backend/data for showcase
- Upgrade path: Railway Hobby or AWS EC2 only if cold starts/persistence become a problem

Answer and document clearly:
- Do we need Kubernetes? No.
- Do we need Jenkins? No.
- Do we need API Gateway? Not for MVP.
- Do we need CDN? Not manually; Cloudflare/Vercel already serve static frontend globally.
- Do we need RDS/Postgres? Not initially; SQLite is okay for demo.
- Do we need Supabase? Not now; use later for Auth/Postgres if login is added.
- Do we need AWS? Not for the first free deployment.

Technical preparation tasks:
1. Inspect current backend/frontend build setup.
2. Verify frontend can use VITE_API_URL for deployed backend URL.
3. Verify backend CORS supports CORS_ORIGINS from env.
4. Verify Docker Compose still works locally.
5. Verify backend/data persistence assumptions are documented.
6. Document free-platform limitations:
   - Render free sleeps and local filesystem is not reliable.
   - Koyeb free has 512 MB RAM, no persistent volumes, sleeps after inactivity.
   - Vercel is best for frontend but not ideal for this Python RAG backend.
   - Hugging Face Spaces is okay for AI demo but disk is stateless unless paid bucket.
7. Add exact deploy steps for:
   - Cloudflare Pages frontend
   - Vercel frontend
   - Render backend
   - Koyeb backend
8. Add env var examples:
   - APP_ENV=production
   - LLM_PROVIDER=none
   - LLM_API_KEY=
   - LLM_MODEL=
   - CORS_ORIGINS=https://your-frontend-url
   - VITE_API_URL=https://your-backend-url
9. Add a warning to never commit API keys.

Acceptance criteria:
- docs/DEPLOYMENT_CHECKLIST.md exists and is step-by-step.
- docs/FREE_DEPLOYMENT_QUICKSTART.md exists and has copy-paste commands/settings.
- No secrets are printed or committed.
- npm run build passes.
- backend pytest passes.
- Local app still works.
```

## Task 8B — AWS EC2 Paid Fallback Deployment Prep

Use only if free deployment is too slow/unreliable.

```text
Task: Prepare AWS EC2 Docker Compose deployment docs/config only. Do not deploy.

Read:
- docs/deployment_strategies.md
- docs/RUNNING.md
- docker-compose.yml
- backend/app/core/config.py

Goal:
Prepare for AWS EC2 + Docker Compose + Caddy HTTPS + persistent backend/data volume.

Tasks:
1. Add docs/AWS_EC2_DEPLOYMENT_CHECKLIST.md.
2. Add sample Caddyfile.
3. Add backup script for backend/data.
4. Verify docker-compose volume mapping for backend/data.
5. Document security group:
   - 22 only from user IP
   - 80/443 public
   - do not expose 8000/5173 publicly
6. Document AWS Budget alert setup.
7. Document t3.small/t4g.small tradeoff.

Acceptance criteria:
- AWS doc is beginner-friendly.
- No secrets.
- Local Docker Compose remains unchanged unless necessary.
- Clear cost warning included.
```

## Copy-Paste Starter Prompt For Claude Now

```text
You are working inside the existing FINTRUST-AI project. This is not a fresh scaffold.

Read first:
- README.md
- docs/RUNNING.md
- docs/00_DECISIONS_AND_STACK.md
- docs/TECHNICAL_IMPLEMENTATION_PLAN.md
- sources/sources.md

Do not read or print secret API keys from docs/API_LLM_API_SDK_KEYS.txt.

Task: Run a current-state audit only. Do not modify files.

Return:
1. Current backend modules implemented.
2. Current frontend pages/components implemented.
3. Current tests/evaluation status.
4. Documentation drift, if any.
5. The next 5 highest-value implementation tasks.
6. Exact commands to run locally.

Important constraints:
- Preserve LLM_PROVIDER=none as default.
- Do not introduce LangChain unless there is a concrete reason.
- Do not ingest all sources.
- Do not mix insurance and banking retrieval.
```

## Copy-Paste Deployment Prompt For Claude

Use this when you are ready to prepare free hosting:

```text
You are working inside the existing FINTRUST-AI project. This is not a fresh scaffold.

Read first:
- README.md
- docs/RUNNING.md
- docs/00_DECISIONS_AND_STACK.md
- docs/deployment_strategies.md
- docker-compose.yml
- backend/app/core/config.py
- backend/requirements.txt
- frontend/package.json

Do not read or print secrets from:
- docs/API_LLM_API_SDK_KEYS.txt
- backend/.env

Task:
Prepare the app for free or near-free public deployment.

Target:
- frontend on Cloudflare Pages or Vercel Free
- backend on Render Free first, Koyeb Free as alternative
- LLM_PROVIDER=none by default
- optional Gemini/Groq key later
- no Kubernetes
- no Jenkins
- no API Gateway
- no RDS/Postgres initially

Create/update:
- docs/DEPLOYMENT_CHECKLIST.md
- docs/FREE_DEPLOYMENT_QUICKSTART.md
- frontend/.env.example if missing
- backend/.env.example if deploy vars are missing

Make sure the docs explain:
- Render free sleeps and filesystem persistence limitations.
- Koyeb free limitations.
- Vercel/Cloudflare are frontend-only options.
- backend/data contains SQLite + Chroma and must be treated carefully.
- how to set VITE_API_URL and CORS_ORIGINS.
- how to use LLM_PROVIDER=none first and add Gemini/Groq later.
- how to avoid committing secrets.

Acceptance criteria:
- npm run build passes.
- backend pytest passes.
- local app still works.
- deployment docs are beginner-friendly and step-by-step.
- no secrets are exposed.

Before editing: summarize a short plan.
After editing: list changed files and exact verification commands.
```
