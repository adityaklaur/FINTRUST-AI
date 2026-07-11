# FinTrust AI

FinTrust AI is a source-grounded financial services copilot for banking, payments, compliance, grievance redressal, and claims-support workflows. The goal is not to build a generic chatbot. The goal is to build a system that answers only from trusted public documents, shows citations, explains uncertainty, classifies the issue, suggests the correct escalation path, and keeps an audit trail.

This repository contains the project proposal, a curated source corpus, **and a working MVP implementation** (FastAPI backend + React frontend).

> ▶ **To run it, see [`docs/RUNNING.md`](docs/RUNNING.md).** It works offline with no API keys (answers are grounded + cited from the corpus); add a free Groq/Gemini key to upgrade the prose. See [`docs/00_DECISIONS_AND_STACK.md`](docs/00_DECISIONS_AND_STACK.md) for why RAG (not model training), which DB, which models, and how to stay current.

## Product Vision

Financial-services customers and internal support teams often struggle with long policy documents, confusing escalation paths, and unclear complaint categories.

Examples:

- A UPI transaction failed but money was debited.
- A credit card complaint was not resolved within 30 days.
- A bank changed EMI or loan tenor after interest-rate reset.
- A customer wants to know whether RBI Ombudsman, Sachet, UDGAM, DICGC, IRDAI, or Insurance Ombudsman is the correct route.
- A nominee/legal heir wants to know what documents are needed after a depositor dies.
- A user needs to understand what evidence is needed for an unauthorized transaction or card dispute.

FinTrust AI should help by retrieving the relevant source passages, generating a cautious answer, showing citations, identifying the complaint type, and recommending the next human-reviewed step.

## Important Safety Position

FinTrust AI must not provide final legal, regulatory, tax, financial, credit, claim-admissibility, or banking advice.

Every response should be framed as:

- A source-grounded explanation.
- A checklist of documents/information needed.
- A suggested escalation route.
- A human-reviewable draft, not a final decision.

The system must refuse or qualify answers when source evidence is insufficient.

## Current Repository Contents

- `FinTrust_AI_Project_Proposal.txt`
  - Full product proposal, source strategy, milestones, pending-source plan, and implementation guidance.
- `sources/`
  - Curated source corpus with RBI, NPCI, bank, insurance, dataset, and research references.
- `sources/sources.md`
  - Source registry, ingestion priority, manual gaps, classifier categories, and corpus status.
- `docs/`
  - Technical implementation documents and Claude prompt pack.
  - `docs/TECHNICAL_IMPLEMENTATION_PLAN.md` — data models, API contracts, ingestion rules.
  - `docs/CLAUDE_IMPLEMENTATION_PROMPT.md` — master context + phase-by-phase prompts.

## Current Source Corpus

The corpus currently includes more than 200 files across:

- RBI and regulatory documents
- NPCI / UPI / RuPay / BBPS references
- Bank-specific policy documents and snapshots
- Insurance / IRDAI expansion sources
- Dataset metadata and research references

The most important implementation file is:

`sources/sources.md`

Use it as the source-of-truth registry for:

- ingestion priority
- domain classification
- metadata design
- manual-source gaps
- evaluation categories

## Recommended MVP Scope

Do not implement every source category in the first version.

The recommended MVP is:

- Banking and payments only
- RBI-first retrieval
- Citations and source chunks
- Complaint classification
- Risk label
- Escalation route
- Audit logging
- Evaluation on a small question set

Recommended first categories:

- `credit_card_grievance`
- `upi_failed_transaction`
- `unauthorized_transaction`
- `ombudsman_escalation`
- `kyc_or_identity`
- `failed_transaction_tat_compensation`
- `support_contact_or_nodal_officer`
- `unsupported_or_advice_request`

Insurance should be a separate module or separate index called `Insurance Claims`, not mixed into the first banking index.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.11 · FastAPI · Pydantic v2 |
| Database | SQLite via SQLModel |
| Vector store | ChromaDB |
| AI / RAG | Direct ChromaDB retrieval · ONNX MiniLM embeddings by default |
| LLM | `LLM_PROVIDER=none` extractive mode by default; Gemini / Groq / OpenAI / Claude optional |
| Frontend | React 18 + TypeScript · Vite · Tailwind CSS |
| Tests | pytest (backend) · Vitest (frontend) |

## Recommended Folder Structure

```text
FINTRUST-AI/
  backend/
    app/
      main.py
      api/          health · query · sources · audit · evaluation
      core/         config · logging · constants · exceptions
      schemas/      query · source · audit · evaluation
      ingest/       discover · loaders · chunker · registry · pipeline
      retrieval/    vector_store · retriever · filters · reranker
      generation/   llm_client · prompts · answer · citations · refusal
      classifier/   taxonomy · classifier · risk · escalation
      storage/      db · source_repo · audit_repo
      evaluation/   dataset · runner · metrics
    data/
      vector_store/
      eval/
      audit/
    tests/
    requirements.txt
    .env.example
    Dockerfile
  frontend/
    src/
      components/   QueryPanel · CitationCard · RiskBadge · EscalationRoute
      pages/        Home · AuditHistory · SourceExplorer · EvalDashboard
      api/          client.ts · types.ts
      hooks/        useQuery · useAudit
    vite.config.ts
    package.json
  sources/
  docs/
  docker-compose.yml
  README.md
```

## Metadata Requirements

Every chunk must carry metadata. Without metadata, the RAG system will mix unrelated rules.

Minimum metadata:

- `source_file`
- `source_url`
- `title`
- `domain`
- `subdomain`
- `authority`
- `institution`
- `document_type`
- `effective_year`
- `is_authoritative`
- `is_bank_specific`
- `is_insurance_specific`
- `chunk_id`

Suggested `domain` values:

- `banking_payments`
- `insurance`
- `research_reference`
- `dataset`

Suggested `authority` values:

- `RBI`
- `NPCI`
- `BANK`
- `IRDAI`
- `DICGC`
- `SACHET`
- `RESEARCH`

## Retrieval Rules

Use source hierarchy:

- First: RBI/NPCI/IRDAI/DICGC authoritative sources
- Second: bank-specific policy sources when a bank is named
- Third: research references only for design notes, not user-facing answers
- Fourth: community/blog/forum content only for product research, never as policy authority

Important:

- If user names a bank, retrieve from both RBI and that bank.
- If user does not name a bank, retrieve RBI/NPCI first.
- If user asks an insurance question, retrieve only insurance sources.
- If the system cannot find supporting text, it should say it does not have enough source context.

## First Implementation Milestones

### Milestone 1: Project Skeleton

Create the application structure, Python environment, basic config, and placeholder FastAPI/Streamlit apps.

Acceptance criteria:

- App starts locally.
- Health endpoint works.
- Frontend shows a simple query box.
- No RAG yet.

### Milestone 2: Source Registry

Build a source registry from files under `sources/`.

Acceptance criteria:

- Script scans `sources/`.
- Each file gets metadata.
- Metadata is saved to SQLite or JSON.
- Bad/unsupported files are skipped with logs.

### Milestone 3: Ingestion

Ingest a small curated set first.

Use only 8-12 initial documents from `sources/sources.md`.

Acceptance criteria:

- Text files and PDFs are loaded.
- Chunks are created.
- Chunk metadata is preserved.
- Chunks are stored in ChromaDB.

### Milestone 4: Basic RAG

Build query to retrieval to answer generation.

Acceptance criteria:

- User asks question.
- System retrieves top chunks.
- Answer includes source citations.
- UI shows retrieved chunks.
- Unsupported questions are refused or qualified.

### Milestone 5: Classification and Risk

Classify the issue and assign risk.

Acceptance criteria:

- Query category returned.
- Risk label returned.
- Escalation route suggested.
- Needed evidence/documents listed.

### Milestone 6: Audit Log

Log every query and result.

Acceptance criteria:

- Store question, category, risk, answer, citations, source IDs, latency, model name, timestamp.
- UI has an audit/history page.

### Milestone 7: Evaluation

Create and run evaluation questions.

Acceptance criteria:

- At least 30 initial evaluation questions.
- Questions cover credit card, UPI, unauthorized transaction, KYC, Ombudsman and unsupported categories.
- Evaluation records retrieval success, faithfulness, citation quality and refusal correctness.

## How To Use Claude Efficiently

The complete phase-by-phase Claude prompt pack lives in:

`docs/CLAUDE_IMPLEMENTATION_PROMPT.md`

Key rules:
- Run **one phase per Claude session**.
- Always start each session by pasting the **Master Context Block** from the prompt file.
- Do not dump the full source corpus into Claude — give only the files each phase needs.
- Each phase has exact acceptance criteria; do not move to the next phase until they pass.

Phases:
1. Project Skeleton (FastAPI + React scaffolding)
2. Source Registry (scan corpus, infer metadata, persist)
3. Ingestion Pipeline (load, chunk, embed 12 seed documents)
4. Retrieval (ChromaDB query + metadata filters)
5. Answer Generation with Citations (LLM grounded on chunks)
6. Classification, Risk & Escalation
7. Audit Logging
8. Evaluation Harness
9. React Frontend (full UI)
10. Polish & Demo Prep

## What Not To Do

- Do not ingest all 200+ files at once.
- Do not mix insurance and banking in one retrieval index without metadata filters.
- Do not use research/blog/community content as authoritative policy source.
- Do not answer claim/legal/financial questions as final advice.
- Do not build agents before basic RAG works.
- Do not fine-tune before the RAG baseline is complete.

## Near-Term Goal

The immediate goal is not a perfect enterprise system.

The immediate goal is:

> A working local demo where a user asks a financial grievance question and receives a cited, source-grounded, cautious answer with category, risk label, evidence checklist and escalation route.

Once that works, expand document coverage and evaluation.
