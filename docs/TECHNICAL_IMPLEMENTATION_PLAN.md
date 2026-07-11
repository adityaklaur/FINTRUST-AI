# FinTrust AI Technical Implementation Plan

This document converts the FinTrust AI proposal and source corpus into an implementation plan.

Primary project files:

- `FinTrust_AI_Project_Proposal.txt`
- `README.md`
- `sources/sources.md`
- `prompts/CLAUDE_IMPLEMENTATION_PROMPT.md`

## 1. Implementation Philosophy

Build a narrow, reliable, source-grounded MVP first.

The dangerous failure mode is a broad chatbot that sounds confident but mixes RBI, bank-specific, NPCI and IRDAI rules incorrectly. The architecture must therefore prioritize:

- metadata filtering
- source ranking
- citation display
- refusal when unsupported
- audit logging
- evaluation before expansion

## 1a. Tech Stack (fixed)

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+ · FastAPI · Pydantic v2 · SQLite (SQLModel) |
| Vector store | ChromaDB |
| AI / RAG | Direct ChromaDB retrieval · ONNX MiniLM embeddings by default |
| LLM | `LLM_PROVIDER=none` extractive mode by default; Gemini / Groq / OpenAI / Claude optional |
| Frontend | React 18 + TypeScript · Vite · Tailwind CSS |
| Tests | pytest (backend) · Vitest (frontend) |
| Dev tools | ruff · black · uvicorn |

The Claude implementation prompt is at: `docs/CLAUDE_IMPLEMENTATION_PROMPT.md`

## 2. Target MVP

The first version should support:

- credit-card grievance
- UPI failed transaction
- unauthorized transaction
- KYC / identity issue
- RBI Ombudsman escalation
- failed transaction TAT / compensation
- support contact / nodal officer route
- unsupported or advice request refusal

Insurance, DICGC, UDGAM, BBPS, loan EMI reset, cheque collection, deceased depositor and bank-specific compensation are already researched, but should be enabled gradually after the MVP works.

## 3. Recommended Folder Structure

```text
FINTRUST-AI/
  backend/
    app/
      main.py
      api/
        health.py
        query.py
        sources.py
        audit.py
        evaluation.py
      core/
        config.py
        logging.py
        constants.py
        exceptions.py
      schemas/
        query.py
        source.py
        audit.py
        evaluation.py
      ingest/
        discover.py
        loaders.py
        chunker.py
        registry.py
        pipeline.py
      retrieval/
        vector_store.py
        retriever.py
        filters.py
        reranker.py
      generation/
        llm_client.py
        prompts.py
        answer.py
        citations.py
        refusal.py
      classifier/
        taxonomy.py
        classifier.py
        risk.py
        escalation.py
      storage/
        db.py
        audit_repo.py
        source_repo.py
      evaluation/
        dataset.py
        runner.py
        metrics.py
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
      components/
      pages/
      api/
      hooks/
      lib/
    package.json
    vite.config.ts
    tailwind.config.ts
  sources/
  docs/
    TECHNICAL_IMPLEMENTATION_PLAN.md
    CLAUDE_IMPLEMENTATION_PROMPT.md
  docker-compose.yml
  README.md
```

## 4. Core Data Models

### Source Document

Fields:

- `source_id`
- `file_path`
- `title`
- `source_url`
- `domain`
- `subdomain`
- `authority`
- `institution`
- `document_type`
- `effective_year`
- `is_authoritative`
- `is_bank_specific`
- `is_insurance_specific`
- `ingestion_status`
- `notes`

### Chunk

Fields:

- `chunk_id`
- `source_id`
- `text`
- `chunk_index`
- `token_count`
- `section_title`
- `page_number`
- `metadata`

### Query Request

Fields:

- `question`
- `selected_domain`
- `selected_institution`
- `user_context`
- `top_k`
- `include_debug`

### Query Response

Fields:

- `answer`
- `category`
- `risk_level`
- `escalation_route`
- `evidence_checklist`
- `citations`
- `retrieved_chunks`
- `unsupported`
- `latency_ms`
- `audit_id`

### Citation

Fields:

- `source_id`
- `source_title`
- `source_file`
- `source_url`
- `section_title`
- `page_number`
- `quote`

### Audit Log

Fields:

- `audit_id`
- `timestamp`
- `question`
- `category`
- `risk_level`
- `answer`
- `citations_json`
- `retrieved_chunks_json`
- `model_name`
- `latency_ms`
- `unsupported`

## 5. Metadata Strategy

Metadata controls answer correctness.

Suggested metadata values:

Domains:

- `banking_payments`
- `insurance`
- `research_reference`
- `dataset`

Authorities:

- `RBI`
- `NPCI`
- `BANK`
- `IRDAI`
- `DICGC`
- `SACHET`
- `RESEARCH`

Bank institutions:

- `hdfc`
- `icici`
- `axis`
- `sbi`
- `kotak`
- `idfc`
- `bob`
- `canara`
- `pnb`
- `union`
- `federal`
- `hsbc`
- `standard_chartered`
- `au`
- `general`

Subdomains:

- `credit_card`
- `debit_card`
- `upi`
- `failed_transaction`
- `unauthorized_transaction`
- `kyc`
- `ombudsman`
- `deposit_account`
- `cheque`
- `locker`
- `deceased_claim`
- `loan`
- `bbps`
- `nach`
- `aeps`
- `fraud_awareness`
- `insurance_health`
- `insurance_life`
- `insurance_motor`
- `insurance_property`

## 6. Initial Source Set

Do not ingest everything first.

Initial ingestion should use roughly:

- `regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt`
- `regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_faq.txt`
- `regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_pdf.pdf`
- `regulatory_rbi/rbi_failed_transactions_tat_compensation_2019_clean_extract.txt`
- `regulatory_rbi/rbi_unauthorized_electronic_banking_customer_liability_2017.txt`
- `regulatory_rbi/rbi_online_dispute_resolution_digital_payments_2020_clean_extract.txt`
- `npci_upi/npci_upi_help_brand_guidelines_2023_extracted.txt`
- `npci_upi/npci_upi_help_assistant_pilot_2025.pdf`
- `bank_documents/hdfc_credit_card_mitc_english_extracted.txt`
- `bank_documents/axis_grievance_redressal_policy_2026_extracted.txt`
- `bank_documents/icici_credit_card_mitc_extracted.txt`
- `bank_documents/sbi_card_customer_grievance_policy_extracted.txt`

This is enough for a strong first demo.

## 7. Ingestion Design

Ingestion steps:

1. Scan selected files.
2. Create source registry entries.
3. Load text from `.txt`, `.md`, `.pdf`, `.html`.
4. Clean boilerplate.
5. Chunk by headings where possible.
6. Attach metadata to every chunk.
7. Embed chunks.
8. Store in ChromaDB.
9. Save ingestion report.

Chunking rule:

- Start with 800 to 1,200 tokens.
- Use 100 to 150 token overlap.
- Preserve headings.
- Avoid mixing multiple unrelated clauses in a huge chunk.

## 8. Retrieval Design

Initial retrieval:

- vector similarity
- metadata filters
- top 6 to 10 chunks

Later:

- BM25 keyword retrieval
- hybrid merge
- reranking

Retrieval filters:

- If domain is insurance, search only `domain=insurance`.
- If bank is named, search RBI plus selected bank.
- If no bank is named, search RBI/NPCI/DICGC first.
- Do not search research references for user-facing answers.

## 9. Answer Generation

Answer prompt must require:

- answer only from retrieved context
- cite sources
- state uncertainty
- refuse unsupported requests
- avoid final legal/financial advice
- include evidence checklist
- include escalation route

Suggested answer structure:

- Short answer
- What the source says
- What you should collect
- Escalation path
- Caveats / human review note
- Citations

## 10. Classification

Start rule-based plus LLM-assisted classification.

Initial categories:

- `credit_card_grievance`
- `upi_failed_transaction`
- `unauthorized_transaction`
- `kyc_or_identity`
- `ombudsman_escalation`
- `failed_transaction_tat_compensation`
- `support_contact_or_nodal_officer`
- `unsupported_or_advice_request`

Risk levels:

- `low`
- `medium`
- `high`

High-risk examples:

- unauthorized transaction
- fraud
- harassment
- money stuck beyond TAT
- complaint unresolved beyond 30 days
- deceased depositor claim
- legal/claim/credit decision requested

## 11. Escalation Logic

Common escalation sequence:

- First: relevant app/bank/insurer/service provider
- Then: nodal/grievance officer where applicable
- Then: regulator or ombudsman if unresolved within required timeline

Examples:

- UPI failed transaction: UPI app/help -> bank/PSP -> RBI CMS if unresolved.
- Credit card grievance: card issuer support -> grievance officer/nodal officer -> RBI Ombudsman.
- Unauthorized bank transaction: report immediately to bank -> bank investigates/shadow reversal where applicable -> RBI CMS if unresolved.
- Insurance claim: insurer GRO -> Bima Bharosa / IRDAI grievance -> Insurance Ombudsman.
- Unauthorized deposit scheme: Sachet, not RBI CMS.

## 12. API Design

Suggested endpoints:

- `GET /health`
- `POST /query`
- `GET /sources`
- `GET /sources/{source_id}`
- `GET /audit`
- `GET /audit/{audit_id}`
- `POST /evaluate/run`

`POST /query` request:

```json
{
  "question": "My UPI payment failed but money was debited. What should I do?",
  "selected_domain": "banking_payments",
  "selected_institution": null,
  "top_k": 8,
  "include_debug": true
}
```

## 13. Frontend Design

Use React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui.

Pages:

- Home (Query assistant)
- Source Explorer
- Audit History
- Evaluation Dashboard

Query page layout:

- Left panel: question textarea, domain selector, bank selector, submit button
- Right panel: answer, category + risk badges, evidence checklist, escalation steps, disclaimer, citations, debug expander

Components to build:
- QueryPanel, AnswerPanel, CitationCard, RiskBadge, CategoryBadge, EscalationRoute, DisclaimerBanner

See `docs/CLAUDE_IMPLEMENTATION_PROMPT.md` Phase 9 for the full component spec.

## 14. Evaluation Plan

Create initial evaluation dataset:

- 30 questions for MVP
- later expand to 100 questions

Evaluate:

- retrieved source correctness
- answer faithfulness
- citation presence
- refusal correctness
- escalation path correctness
- category correctness

Initial eval categories:

- credit card 30-day grievance
- UPI T+1/T+5 failed payment
- unauthorized transaction reporting
- KYC update
- Ombudsman eligibility
- unsupported legal/financial advice

## 15. Implementation Phases For Claude

Use the prompt pack:

`prompts/CLAUDE_IMPLEMENTATION_PROMPT.md`

Do not ask Claude to build everything in one prompt.

Use one phase per session:

1. Project skeleton
2. Source registry
3. Ingestion pipeline
4. Vector retrieval
5. Answer generation and citations
6. Classification and risk
7. Audit logging
8. Evaluation harness
9. Frontend polish
10. Deployment preparation

## 16. Definition Of Done For MVP

MVP is done when:

- user can ask a question
- system retrieves sources
- answer has citations
- answer includes category and risk
- answer suggests escalation route
- answer lists required evidence
- unsupported questions are refused
- query is audit logged
- at least 30 evaluation questions run

## 17. Common Mistakes To Avoid

- Ingesting all files too early.
- Ignoring metadata.
- Mixing bank-specific documents with general RBI answers.
- Using research articles as answer sources.
- Letting the LLM answer from memory.
- Overbuilding agents before RAG works.
- Skipping evaluation.

## 18. Recommended Immediate Task

Start with Phase 1 and Phase 2:

- create skeleton
- implement source registry
- ingest 8-12 documents only

Only after those work should retrieval and generation begin.





