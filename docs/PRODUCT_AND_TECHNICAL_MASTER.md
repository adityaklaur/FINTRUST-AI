# FinTrust AI — Product & Technical Master Document

> One combined reference: what this product is, the problem it solves, why it is
> trustworthy, an honest comparison to ChatGPT/Gemini/Grok, what is built vs.
> planned, the full technical picture (stack, flow, patterns, APIs), the
> decisions for going to real users, and the prioritized backlog.
>
> Last updated: 2026-07-11 · Status: working MVP, pre-deployment.

## Table of contents
- [Part 1 — Product](#part-1--product)
  - [1. What FinTrust AI is](#1-what-fintrust-ai-is)
  - [2. The problem](#2-the-problem)
  - [3. What it solves and why the industry needs it](#3-what-it-solves-and-why-the-industry-needs-it)
  - [4. How it solves it better](#4-how-it-solves-it-better)
  - [5. Why it is trustworthy](#5-why-it-is-trustworthy)
  - [6. Honest positioning: "GPT/Gemini/Grok are more powerful — so why this?"](#6-honest-positioning-gptgeminigrok-are-more-powerful--so-why-this)
- [Part 2 — What's built vs. what's coming](#part-2--whats-built-vs-whats-coming)
- [Part 3 — Technical](#part-3--technical)
  - [9. Tech stack & libraries (what and why)](#9-tech-stack--libraries-what-and-why)
  - [10. Architecture & request flow](#10-architecture--request-flow)
  - [11. Repository structure](#11-repository-structure)
  - [12. Design patterns (used + recommended)](#12-design-patterns-used--recommended)
  - [13. APIs we use today](#13-apis-we-use-today)
- [Part 4 — Decisions for real users](#part-4--decisions-for-real-users)
  - [14. Database](#14-database-decision)
  - [15. Auth & per-user audit](#15-auth--per-user-audit-decision)
  - [16. LLM strategy](#16-llm-strategy-free-first-upgradable)
  - [17. Public data & government APIs](#17-public-data--government-apis-to-leverage)
  - [18. Staying current (NOT training)](#18-staying-current-the-refresh-pipeline-not-training)
  - [19. Deployment](#19-deployment-decision)
  - [20. Integrations cheat-sheet](#20-integrations-cheat-sheet-keys-env-vars-callback-urls)
- [Part 5 — Must-do improvements (prioritized)](#part-5--must-do-improvements-prioritized)
- [Sources](#sources)

---

# Part 1 — Product

## 1. What FinTrust AI is

**FinTrust AI is a source-grounded copilot for financial-services grievances and
compliance questions.** A user asks something like *"my UPI payment failed but
money was debited"* or *"my credit-card complaint wasn't resolved in 30 days"*,
and it returns:

- a cautious, plain-language answer **assembled only from trusted public
  documents** (RBI, NPCI, bank policies),
- **inline citations** to the exact source passages,
- the **issue category** and a **risk level**,
- an **escalation route** (who to contact, in what order, with the real portal),
- an **evidence checklist** (what documents to gather),
- and a **refusal** when the sources don't support an answer.

It is **not a generic chatbot**. It will not give financial/legal advice, and it
will not answer from an LLM's memory.

## 2. The problem

Financial-services customers and the support teams that serve them drown in
long, fragmented, frequently-updated regulation:

- Rules live across hundreds of PDFs (RBI Master Directions, RB-IOS 2026, NPCI
  circulars, per-bank MITC/grievance policies) that ordinary users never read.
- The **escalation path is confusing**: bank → nodal officer → RBI CMS →
  Ombudsman, or for insurance GRO → Bima Bharosa → Insurance Ombudsman, or for
  unauthorized schemes → Sachet, not RBI. People go to the wrong place and lose
  time and money.
- Generic chatbots **hallucinate deadlines and entitlements** ("you'll get a
  refund in 24 hours") that aren't in any rule — dangerous in a money context.
- Support agents give **inconsistent answers** with no citation and no audit
  trail — a compliance problem for the institution.

## 3. What it solves and why the industry needs it

| Pain | FinTrust AI's answer |
|---|---|
| "Which rule applies and what does it actually say?" | Retrieves the exact clause and **quotes + cites** it. |
| "Where do I complain, and when am I eligible?" | Deterministic **escalation route** grounded in RB-IOS 2026 / IRDAI rules. |
| "What do I need to prepare?" | Category-specific **evidence checklist**. |
| "Is this urgent?" | **Risk label** (fraud/deceased-claim/money-stuck ⇒ high). |
| "Can we trust and defend this answer?" | **Citations + audit log** for every response. |
| "Can we use AI without leaking customer data to OpenAI?" | Runs on **your** corpus, your infra, offline-capable. |

The industry need is real: banks, PSPs, insurers, and BFSI BPOs all run large
grievance-support operations under regulatory scrutiny (RBI/IRDAI). They need
answers that are **grounded, consistent, auditable, and safe** — not "clever."

## 4. How it solves it better

1. **Retrieval before generation.** Every answer starts from retrieved passages
   in a curated vector store; the model may only phrase what the sources say.
2. **Metadata-aware retrieval.** Chunks carry `authority` (RBI/NPCI/BANK/IRDAI),
   `institution`, `domain`. Banking queries never pull insurance rules; research
   blogs are never used as authority; a named bank pulls RBI **plus** that bank.
3. **Refuse-by-default.** If the top match is weak (score < threshold) or the
   question is an advice request, it refuses with helpful next steps instead of
   guessing.
4. **Structured domain output.** Category, risk, escalation, and evidence are
   produced by a **deterministic, code-owned** taxonomy — not left to a model —
   because a wrong ombudsman route is worse than a clumsy sentence.
5. **Audit trail.** Every query is logged (question, category, risk, sources,
   model, latency) for review and improvement.

## 5. Why it is trustworthy

The "trust stack", from bottom to top:

```
Curated authoritative corpus (RBI/NPCI/bank)          <- you control what's authoritative
  → metadata tagging (authority/domain/institution)   <- prevents rule mixing
    → filtered vector retrieval + score floor         <- only relevant, strong matches
      → deterministic classifier/risk/escalation      <- safety-critical logic in code, not the LLM
        → grounded generation, citation-required      <- model phrases; sources decide
          → mandatory refusal + disclaimer            <- never fake advice
            → audit log                                <- every answer is accountable
```

No single layer is novel; the **discipline of stacking all of them** is what
makes the output defensible in a regulated context.

## 6. Honest positioning: "GPT/Gemini/Grok are more powerful — so why this?"

**Straight answer:** frontier chatbots (GPT-5, Gemini, Grok) are more fluent,
broader, and far better reasoners than FinTrust AI. We are **not** trying to beat
them at general intelligence, and pretending otherwise would be dishonest.

FinTrust AI competes on a **different axis — trust and control — inside a narrow
domain**, and there it genuinely wins:

| Dimension | Frontier chatbot (GPT/Gemini/Grok) | FinTrust AI |
|---|---|---|
| General reasoning / fluency | ✅ Superior | ➖ Adequate (better with an LLM key) |
| Grounded in *authoritative Indian BFSI* sources | ⚠️ Only if it browses; often generic/global | ✅ By construction |
| Exact citations to the clause | ⚠️ Inconsistent | ✅ Every factual claim |
| Refuses when unsupported | ⚠️ Tends to answer anyway | ✅ Enforced |
| Deterministic escalation/risk/evidence | ❌ Varies per prompt | ✅ Code-owned, consistent |
| Audit trail for compliance | ❌ Not by default | ✅ Built in |
| Data control / privacy (no data sent to a 3rd party) | ❌ Sent to the provider | ✅ Can run offline / in-house |
| Cost at scale | 💲 Per-token | ✅ $0 in `none` mode; cheap otherwise |
| Always up to date on *your* rulebook | ⚠️ Training-cutoff + generic | ✅ Refresh pipeline on your corpus |

**Where a frontier model still wins, honestly:** with web browsing and a good
prompt it can *approximate* a lot of this for a one-off consumer question. Our
edge is **not raw IQ** — it is provenance, refusal, consistency, auditability,
privacy, and cost. Those are exactly the properties that matter when the "user"
is a **bank's support desk, an ombudsman helpline, or a BFSI BPO** that must be
correct, consistent, and accountable — and that cannot paste customer data into
ChatGPT.

**The genuine one-line pitch:** *"Not the smartest AI — the one a compliance
officer will actually sign off on."*

**Where we are honestly weak today** (and how we fix it): small corpus (12 docs →
expand via the refresh pipeline); templated prose in `none` mode (add a free
LLM key); no login/per-user history yet (Supabase Auth next). See Part 5.

---

# Part 2 — What's built vs. what's coming

**Legend:** ✅ done & verified · 🔜 next (designed, not built) · 🔭 later (vision)

| Capability | Status | Notes |
|---|---|---|
| Source registry (232 docs) | ✅ | filename→metadata inference, SQLite |
| Ingestion → ChromaDB (550 chunks / 12 docs) | ✅ | ONNX embeddings, no torch |
| Metadata-filtered retrieval + refusal floor | ✅ | RBI-first, bank-aware, insurance-isolated |
| Classification + risk + escalation + evidence | ✅ | 16 categories, deterministic |
| Grounded answer + citations + disclaimer | ✅ | offline extractive or LLM |
| Audit logging | ✅ | global (not yet per-user) |
| Evaluation harness (32 Q) | ✅ | 100% category/refusal/disclaimer |
| React UI (Assistant/Audit/Sources/Eval) | ✅ | Tailwind v4, react-query |
| Optional LLM (Groq/Gemini/OpenAI/Anthropic) | ✅ | env-switchable, safe fallback |
| **LLM failover (Groq→Gemini→offline)** | ✅ | `LLMRouter`; add a free key to activate |
| **Document refresh pipeline (RBI RSS)** | ✅ | detect + manual/API re-ingest; `app/ingest/refresh.py` + `/api/updates` |
| **User login + per-user audit history** | ✅ | Supabase Auth, config-gated; default stays anonymous (see §15) |
| **Postgres support (Supabase/Neon)** | ✅ | `DATABASE_URL` env; default stays SQLite (see §14) |
| **Deploy configs (Render + Vercel)** | ✅ | `render.yaml`, `frontend/vercel.json`, `docs/DEPLOYMENT_CHECKLIST.md` |
| **Scheduled auto-refresh (cron)** | 🔜 | daily job calling `app.ingest.refresh` |
| **Actually deployed public URL** | 🔜 | configs ready; one deploy away (see §19) |
| Hybrid retrieval (BM25 + vector) + reranker | 🔜 | recall/precision boost |
| Corpus expansion (KYC, insurance, more banks) | 🔜 | already downloaded, not ingested |
| Answer feedback (👍/👎) loop | 🔜 | improve retrieval/eval |
| Gov API enrichment (API Setu / data.gov.in) | 🔭 | live reference data |
| Multi-tenant (per-bank), admin, roles | 🔭 | B2B |
| Streaming + conversation memory | 🔭 | UX |
| Fine-tuning | 🔭 | only if grounded RAG proves insufficient — likely never for MVP |

> **Roadmap honesty rule:** the UI marks 🔜/🔭 items clearly as "Coming soon /
> Planned". We never show a control that pretends to work.

---

# Part 3 — Technical

## 9. Tech stack & libraries (what and why)

| Layer | Choice | Why this (and not the alternative) |
|---|---|---|
| API framework | **FastAPI** + Uvicorn | async, typed, auto OpenAPI docs; standard for Python AI backends |
| Validation | **Pydantic v2** | request/response contracts, settings from env |
| Relational store | **SQLite via SQLModel** | zero-setup for MVP; SQLModel = Pydantic+SQLAlchemy, so one model type. Swap to Postgres later by changing the URL |
| Vector store | **ChromaDB** | embedded (no server), metadata filtering, cosine search |
| Embeddings | **ChromaDB built-in ONNX all-MiniLM-L6-v2** | free, local, **no torch** (~80 MB). `sentence-transformers` optional upgrade |
| LLM (optional) | **Groq / Gemini / OpenAI / Anthropic** via their SDKs | env-switchable; **not required** — `none` mode works offline |
| Frontend | **React 18 + TypeScript + Vite 6 + Tailwind v4** | fast dev, typed, modern styling |
| Data fetching | **@tanstack/react-query** + axios | caching, loading/error states |
| Tests / lint | **pytest**, **ruff** | fast, standard |

**Deliberately NOT used:** LangChain (heavy, churns fast — we call Chroma + SDKs
directly), torch (ONNX embedder covers it), a separate vector server (Chroma
embedded is enough at this scale).

## 10. Architecture & request flow

```
                         Browser (React SPA)
                               │  POST /api/query {question, domain, institution}
                               ▼
        ┌──────────────────────────────────────────────────────┐
        │                    FastAPI (app/main.py)               │
        │  routers: health · query · sources · audit · evaluation│
        └───────────────┬────────────────────────────────────────┘
                        ▼
             AnswerGenerator.generate()   (app/generation/answer.py)
                        │
      1. Classifier.classify(question) ──► category  (keyword + priority)
                        │  (advice? → refuse early)
      2. Retriever.retrieve(q, domain, institution)      (app/retrieval)
                        │      │ build_chroma_filter() → authority/domain rules
                        │      ▼
                        │   ChromaDB.query()  → top-k chunks + cosine score
                        │  (best score < 0.35 → refuse)
      3. get_risk_level / get_escalation / get_evidence  (app/classifier)
      4. LLM available? ── yes ─► llm_client.complete(system, context)
                        └─ no  ─► extractive_answer(chunks)   ← offline default
      5. build_citations()  → [Source N] mapped to chunks
      6. QueryResponse(answer+disclaimer, category, risk, escalation,
                       evidence, citations, low_confidence, latency)
      7. audit_repo.insert_audit(...)  → SQLite   → audit_id
                        ▼
                 JSON response → React renders badges, answer, citations
```

**Two data stores:** SQLite (`backend/data/fintrust.db`) for the source registry
+ audit log; ChromaDB (`backend/data/vector_store/`) for embedded chunks.

## 11. Repository structure

```
FINTRUST-AI/
  backend/
    app/
      main.py            # app + router wiring + exception handlers
      api/               # health, query, sources, audit, evaluation
      core/              # config (env), constants, logging, exceptions
      schemas/           # Pydantic/SQLModel: source, chunk, query, retrieval, audit, evaluation
      ingest/            # discover → loaders → chunker → pipeline → registry
      retrieval/         # vector_store, filters, retriever, reranker
      generation/        # llm_client, prompts, answer, citations, refusal
      classifier/        # taxonomy, classifier, risk, escalation
      storage/           # db, source_repo, audit_repo
      evaluation/        # dataset, metrics, runner
    data/                # SQLite + Chroma + eval reports (bundled for demo)
    tests/               # 65 pytest tests
  frontend/src/          # api/ hooks/ components/ pages/ App.tsx
  sources/               # the corpus (RBI/NPCI/bank/insurance/…) + sources.md
  docs/                  # this doc + decisions, running, deployment, phases/
  docker-compose.yml
```

**Flow of a new source → answerable:** `sources/*` → `discover.py` (metadata) →
`registry` (SQLite) → `pipeline.py` (load→chunk→embed) → ChromaDB → retrievable.

## 12. Design patterns (used + recommended)

**Currently in use (good — keep):**
- **Layered architecture** (api → generation/retrieval/classifier → storage). Clear
  boundaries; easy to test each layer.
- **Repository pattern** (`source_repo`, `audit_repo`) — storage hidden behind
  functions; swapping SQLite→Postgres touches only these.
- **Strategy pattern** (`llm_client` picks provider at runtime by env).
- **Factory + singleton** (`get_retriever`, `get_answer_generator` via `lru_cache`).
- **Pipeline** (ingestion stages).
- **Dependency injection** (FastAPI, constructor-injected retriever/llm).

**Recommended additions for our situation (a small team heading to real users):**
- **Ports & Adapters (light hexagonal)** for the three external-ish dependencies
  — vector store, relational store, LLM. Define a thin interface, keep Chroma /
  SQLite / provider SDKs as adapters. This makes "SQLite→Postgres", "Chroma→
  Qdrant", "add OpenRouter" one-file changes. (We're ~70% there already.)
- **Service layer** object (e.g., `QueryService`) so the API router stays thin and
  auth/rate-limit/feedback concerns compose cleanly.

**Explicitly avoid now:** microservices, event sourcing, full DDD, CQRS. They add
operational cost with no payoff at this size. Revisit only at real scale.

## 13. APIs we use today

**Internal (our REST API):**
- `GET /api/health` · `POST /api/query` · `POST /api/query/debug`
- `GET /api/sources` · `GET /api/sources/{id}` · `POST /api/sources/scan` · `POST /api/ingest`
- `GET /api/audit` · `GET /api/audit/{id}`
- `POST /api/evaluation/run` · `GET /api/evaluation/latest`

**External APIs today: none.** Embeddings are local (ONNX); the LLM is optional.
This is a feature — the app runs with zero third-party calls. Planned external
integrations are in Part 4.

---

# Part 4 — Decisions for real users

Every "there are many alternatives — which one?" question, decided for our use case.

## 14. Database (decision)

| Need | Now | Decision for real users |
|---|---|---|
| Source registry + audit | SQLite | **Postgres on Supabase** (free 500 MB, bundles Auth) |
| Vectors | ChromaDB (local) | **Keep Chroma**; move to **Qdrant Cloud** only past ~100k chunks |

**Why Supabase over Neon:** both give free Postgres, but Supabase also gives us
**Auth** (which we need for per-user history) in the same free project — one
integration instead of two. Neon is the better pick *if* we only wanted Postgres.

**How we use it (no code rewrite):** our `storage/` uses SQLModel; switching is
mostly changing `SQLITE_PATH`/URL to a `DATABASE_URL` env var pointing at
Supabase Postgres, and running table creation. The repository pattern means the
rest of the app is untouched.
```env
# backend/.env  (Supabase → Project Settings → Database → Connection string)
DATABASE_URL=postgresql+psycopg://postgres:<pwd>@db.<ref>.supabase.co:5432/postgres
```

## 15. Auth & per-user audit (decision)

**Per-user audit requires identity.** Decision: **Supabase Auth** (email +
Google OAuth), free to 50k MAU, with basic MFA.

**Why not build our own JWT/login?** Auth is a security minefield (password
storage, resets, OAuth, sessions). For a startup MVP, using a managed provider is
faster and safer than hand-rolling it.

**Integration shape:**
```
React → Supabase JS SDK → user signs in (Google/email) → gets a JWT
React → sends `Authorization: Bearer <supabase_jwt>` to FastAPI
FastAPI → verifies the JWT (Supabase JWKS/secret) → extracts user_id
AnswerGenerator → stamps user_id on the AuditEntry
GET /api/audit → filtered to the caller's user_id
```
- **Callback/redirect URLs to register in Supabase** (Auth → URL Config):
  `http://localhost:5173`, `http://localhost:5173/auth/callback`, and the
  deployed frontend URL + `/auth/callback`.
- New env: `SUPABASE_URL`, `SUPABASE_ANON_KEY` (frontend), `SUPABASE_JWT_SECRET`
  (backend, to verify tokens). **Never** put the service-role key in the frontend.
- DB change: add `user_id` to `audit_log`; add a `feedback` table later.

## 16. LLM strategy (free-first, upgradable)

**Decision: keep `none` as the safe default, add Groq as the primary free LLM,
Gemini as fallback, and OpenRouter as an aggregator for experiments.**

| Provider | Free tier (2026) | Default model | Use |
|---|---|---|---|
| `none` | ∞ | — (extractive) | reliability floor, offline demo |
| **Groq** | no card; ~1,000 req/day, fast | `llama-3.3-70b-versatile` | **primary** fluent answers |
| **Gemini** | no card; ~250–1,500 req/day | `gemini-2.5-flash` | fallback, long context |
| OpenRouter | 50/day (1,000 if ≥$10 topped-up) | `:free` models | many models, one key |
| OpenAI / Anthropic | paid API (separate from ChatGPT/Claude subs!) | `gpt-*-mini` / Claude Haiku | polished, paid |

- **Important:** a ChatGPT Plus / Claude subscription does **not** include API
  access — the API is billed separately. Start with Groq/Gemini free keys.
- **Model IDs live in `LLM_MODEL`** and default per provider in
  `llm_client.py`; update there when providers deprecate models.
- **Failover (planned):** try primary → on rate-limit/error, fall to secondary →
  finally to `extractive`. The app already degrades safely to extractive today.
- **Grok (xAI):** available via its own API / OpenRouter; add as another Strategy
  adapter when budget/keys exist. No architectural change needed.

## 17. Public data & government APIs to leverage

| Source | What | How we use it |
|---|---|---|
| **RBI RSS feeds** (`rbi.org.in/notifications_rss.xml`, press/publications) | machine-readable list of new notifications | **primary "new document" trigger** (see §18) |
| **API Setu** (`apisetu.gov.in`, 4,200+ APIs) | gov API gateway | future: verified reference data / DigiLocker-style flows |
| **data.gov.in** (OGD) | open datasets/APIs (needs a free API key) | future: reference datasets, stats |
| Public API directories (public-apis, APIs.guru) | discovery | finding more free/no-auth data |

For our MVP the **RBI RSS feed is the important one** — it directly answers "how
do we know when new rules drop." The rest are enrichment for later.

## 18. Staying current: the refresh pipeline (NOT training)

> This is the honest answer to "how do we train on newly released docs." **We
> don't train. We re-ingest.** Because answers come from retrieved text at query
> time, adding a document to the vector store instantly makes it answerable — no
> weights change, no GPUs, no cost.

**How it works (designed; 🔜 to build):**
```
[scheduled job, e.g. daily]
  1. FETCH   RBI notifications RSS  (rbi.org.in/notifications_rss.xml)
  2. DIFF    each item's link/date vs. the source registry (SQLite)
  3. NEW?    download the PDF/HTML for items we don't have
  4. INGEST  discover metadata → chunk → embed → upsert into ChromaDB
  5. VERIFY  run the eval harness; a query about the new topic now cites it
  6. REPORT  log what was added; surface "corpus updated on <date>" in the UI
```
- **Detection:** RSS `pubDate` + link is the change signal (no scraping needed).
- **No new dependency:** `httpx` (already installed) + stdlib XML parsing.
- **Human-in-the-loop option:** step 3 can require approval before ingesting, so
  we never silently add an unvetted document as "authoritative."
- **Making sure it "works on updated data":** the eval harness is the guardrail —
  add a golden question for the new topic; if `source_hit` and citations pass,
  the update is verified.
- **Scheduling:** a cron job (GitHub Actions on a schedule, or the host's cron)
  calls `python -m app.ingest.refresh`. No always-on worker needed.

**When would we ever actually train/fine-tune?** Only if, after strong retrieval,
the *phrasing/format* is still inadequate at scale — and even then, prompt-tuning
comes first. For a citations-first product, fine-tuning is near the bottom of the
backlog.

## 19. Deployment (decision)

Your `docs/deployment_strategies.md` already covers this in depth; the decision:

- **Frontend → Vercel or Cloudflare Pages (free).** Static Vite build; global CDN.
- **Backend → Render Free (start) → Fly.io/Railway ($5) if cold starts annoy.**
- **LLM → `none` first, then a free Groq/Gemini key.**
- **Data → bundle `backend/data` for the first showcase; move audit/registry to
  Supabase Postgres when login lands (persistence on free hosts is ephemeral).**
- **No Kubernetes / Jenkins / API Gateway / RDS now.**

Frontend already supports `VITE_API_URL`; backend already reads `CORS_ORIGINS`
from env — so deployment is mostly setting env vars, not code changes.

## 20. Integrations cheat-sheet (keys, env vars, callback URLs)

| Integration | Where to get it | Env var(s) | Notes |
|---|---|---|---|
| Groq LLM | console.groq.com | `LLM_PROVIDER=groq`, `LLM_API_KEY`, opt `LLM_MODEL` | free, no card |
| Gemini LLM | aistudio.google.com/apikey | `LLM_PROVIDER=gemini`, `LLM_API_KEY` | free tier |
| OpenRouter | openrouter.ai/keys | `LLM_PROVIDER=openai`-compatible base + key | one key, many models |
| Supabase (DB+Auth) | supabase.com dashboard | `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY` (FE), `SUPABASE_JWT_SECRET` (BE) | anon key is public; service-role key stays server-only |
| Frontend → backend | your deploy | `VITE_API_URL` (FE), `CORS_ORIGINS` (BE) | already wired |
| data.gov.in | data.gov.in signup | `DATA_GOV_IN_API_KEY` | future enrichment |

**Callback URLs to register (Supabase Auth):** local `http://localhost:5173` +
deployed frontend URL, each with `/auth/callback`. **Secrets rule:** only in
`.env` / host secret store; never committed; never in the frontend bundle except
the explicitly-public anon key.

---

# Part 5 — Must-do improvements (prioritized)

**P0 — before real users (trust, safety, persistence):**
1. **Persistence on deploy** — move audit + registry to Supabase Postgres (free
   hosts wipe SQLite on restart). [§14]
2. **Auth + per-user audit** — Supabase Auth; stamp `user_id`; filter history. [§15]
3. **Wire a free LLM** (Groq) with safe fallback to extractive. [§16]
4. **Rate limiting + input caps** on `/api/query` (abuse/cost protection).
5. **Secrets hygiene** — verify nothing sensitive is committed; host env only.

**P1 — quality & freshness:**
6. **Document refresh pipeline** (RBI RSS → re-ingest) + scheduled job. [§18]
7. **Expand corpus** (KYC, insurance, more banks — already downloaded).
8. **Hybrid retrieval** (BM25 + vector) + a cross-encoder reranker.
9. **Answer feedback (👍/👎)** captured to a table → feeds eval & retrieval tuning.
10. **Observability** — structured logs + error tracking (e.g., Sentry free).

**P2 — scale & polish:**
11. Multi-tenant (per-bank corpora), admin dashboard, roles.
12. Streaming responses + light conversation memory.
13. Gov-API enrichment (API Setu / data.gov.in).
14. Fine-tuning — only if grounded RAG is proven insufficient (unlikely for MVP).

---

# Sources

Current-facts research (2026) used for the decisions above:
- Groq free tier & models — [GroqDocs models](https://console.groq.com/docs/models), [GroqDocs rate limits](https://console.groq.com/docs/rate-limits)
- Gemini free tier — [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- Supabase free tier — [Supabase pricing](https://supabase.com/pricing)
- Neon free tier — [Neon plans](https://neon.com/docs/introduction/plans)
- OpenRouter free models — [OpenRouter pricing](https://openrouter.ai/pricing)
- RBI machine-readable feed — [RBI Notifications](https://www.rbi.org.in/Scripts/NotificationUser.aspx) (RSS: `https://www.rbi.org.in/notifications_rss.xml`)
- Government APIs — [API Setu](https://www.apisetu.gov.in/), [data.gov.in APIs](https://www.data.gov.in/apis)
