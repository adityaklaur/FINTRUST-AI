# FinTrust AI — Engineering Decisions & Your Questions Answered

This doc answers the four questions you raised and records the technical
decisions made during implementation, with the *why* behind each so you can
defend or change them later.

---

## Q1. "Which library to use to **train** a model?"

**None. You are not training a model — and you should not.**

FinTrust AI is a **RAG** (Retrieval-Augmented Generation) system. The pipeline is:

```
question ──▶ embed ──▶ search vector DB ──▶ get top text chunks
                                              │
                    ┌─────────────────────────┘
                    ▼
        stuff chunks into a prompt ──▶ hosted LLM ──▶ grounded answer + citations
```

The "intelligence" comes from two pre-trained models you **use as-is**:

1. An **embedding model** (turns text into vectors for search) — runs locally.
2. A **generation LLM** (writes the answer) — hosted API, no training.

Training/fine-tuning would mean collecting labelled data, GPUs, eval loops, and
weeks of iteration — and your own docs explicitly say *"Do not fine-tune before
the RAG baseline is complete."* Fine-tuning is a **much** later optimisation, and
90% of production "AI assistants" never need it. RAG + good prompts + good
retrieval gets you most of the way.

> **Lesson:** "Add knowledge to an LLM" almost always means *retrieval*, not
> *training*. Training changes the model's weights; retrieval changes what you
> put in the prompt. Reach for retrieval first — it's cheaper, faster, auditable,
> and updates the instant you add a document.

---

## Q2. "Which **database** to use?"

**Two databases, each for a different job. Both already correct in your plan.**

| DB | Type | Stores | Why this one |
|----|------|--------|-------------|
| **SQLite** (via SQLModel) | Relational (rows) | source registry, audit log, eval reports | Zero-setup, single file, ships with Python. Perfect for a local/MVP. Swap the connection string for Postgres later with ~no code change. |
| **ChromaDB** | Vector | embedded text chunks + metadata | Purpose-built for semantic search. Runs embedded in-process (no server). Metadata filtering (`authority`, `institution`, `domain`) is exactly what our retrieval rules need. |

**Why two?** They answer different questions. SQLite answers *"show me every query
from Tuesday"* (structured filter). Chroma answers *"which passages are semantically
closest to this question"* (vector similarity). One DB cannot do both well.

**When to graduate:** SQLite → Postgres when you need concurrent writers or
multi-user. Chroma → pgvector/Qdrant/Weaviate when the corpus is >100k chunks or
you need a hosted cluster. For this MVP, neither move is needed.

---

## Q3. "Remaining **models** — which ones?"

Only two kinds, both swappable via env vars:

### Embedding model (local, free, no key)
- **Default: `all-MiniLM-L6-v2`** (sentence-transformers). 384-dim, ~80MB, fast on CPU. The industry default first choice.
- Upgrade path if retrieval quality is weak: `BAAI/bge-small-en-v1.5` or `intfloat/e5-small-v2` — drop-in, just change `EMBEDDING_MODEL`.
- **Rule:** whatever model you ingest with, you must query with. Re-ingest if you change it.

### Generation LLM (hosted, pick one via `LLM_PROVIDER`)
| Provider | Cost | Get a key | Good default model |
|----------|------|-----------|--------------------|
| **`none`** (default) | Free, offline | — | Extractive: answer stitched from chunks, no LLM call |
| **`groq`** | Free tier, very fast | console.groq.com | a current Llama-3.x / GPT-OSS instruct model |
| **`gemini`** | Free tier | aistudio.google.com/apikey | a current Gemini *Flash* model |
| **`openai`** | Paid | platform.openai.com | a current *mini* tier model |
| **`anthropic`** | Paid | console.anthropic.com | Claude Haiku (cheap/fast) |

**Recommendation for you:** start with `none` (works today, zero setup), then get a
**free Groq or Gemini key** to see LLM-quality answers. You do not need a paid key
for the demo. Exact model IDs are set in `backend/app/generation/llm_client.py` and
overridable with `LLM_MODEL` — because providers rename/deprecate models often
(see Q4).

---

## Q4. "How to stay **up to date**?"

Concrete habits baked into this project:

1. **Isolate + pin.** Everything installs into `backend/.venv`. After a working
   install we `pip freeze` into `requirements.txt` so the build is reproducible.
   Upgrading is then a *deliberate* act, not an accident.
2. **One knob per volatile thing.** Model names live in **env vars**
   (`LLM_MODEL`, `EMBEDDING_MODEL`), not scattered in code. Provider deprecates a
   model? Change one line.
3. **Read live docs, not memory.** Library APIs (FastAPI, Chroma, provider SDKs)
   change. Check the official docs / release notes for the version you pinned.
4. **Check the provider's "models" page before shipping.** LLM IDs churn fastest.
   Never hardcode a model ID as the *only* copy.
5. **Upgrade on a cadence, behind tests.** `pytest` + the eval harness (Phase 8)
   are your safety net: bump a version, run evals, compare the score.

---

## Decision log (deviations & choices)

### D1. Dropped LangChain (deviation from the "fixed" stack)
**What:** the plan lists LangChain 0.3; this build does **not** use it.
**Why:** for a retrieve→prompt→generate MVP, LangChain adds a large, fast-churning
dependency surface (its APIs move between minor versions) for almost no benefit.
We call `chromadb`, `sentence-transformers`, and the provider SDKs directly —
fewer moving parts, easier to debug, and directly serves your "stay up to date"
goal. **Revisit** LangChain/LangGraph only when you add multi-step *agents*
(your docs say: not before RAG works).

### D2. `LLM_PROVIDER=none` default (offline extractive answerer)
**What:** the app answers with **no API key** by stitching the top retrieved
chunks into a structured, cited response.
**Why:** you were unsure which model to use. This removes the blocker entirely —
retrieval, citations, classification, risk, and escalation are all real and
testable today; only the *prose* is templated. Add a key later to upgrade it.

### D3. Python 3.13 in a venv
**What:** system Python is 3.9.6 (too old for Chroma/embeddings); we use the
Homebrew **Python 3.13** in an isolated `.venv`.
**Why:** modern, supported, and isolation keeps your system Python untouched.

### D4. Data-dir paths resolved to the backend folder, not CWD
**What:** SQLite + Chroma paths are computed relative to `backend/`.
**Why:** `uvicorn`, `pytest`, and CLI scripts then all agree on file locations no
matter where you run them — a classic source of "works here, not there" bugs.
