# Phases 2 & 3 — Source Registry + Ingestion ✅

## Phase 2 — Source Registry
Scans `sources/`, infers metadata from folder + filename (no LLM), persists to SQLite.

**Files:** `schemas/source.py`, `ingest/discover.py`, `storage/db.py`,
`storage/source_repo.py`, `api/sources.py`, `ingest/registry.py`.

**Result:** 232 sources classified —
banking_payments 197 · insurance 23 · research 10 · dataset 2;
RBI 93 · BANK 87 (17 institutions) · NPCI 15 · IRDAI 13 · RESEARCH 12 · INSURER 10 · DICGC 2.

```bash
cd backend
.venv/bin/python -m app.ingest.registry          # prints classification tables
curl "http://localhost:8000/api/sources?authority=RBI"
```

## Phase 3 — Ingestion Pipeline
Load → clean → chunk (heading-aware, overlap) → embed (ONNX MiniLM) → ChromaDB.

**Files:** `schemas/chunk.py`, `ingest/loaders.py`, `ingest/chunker.py`,
`retrieval/vector_store.py`, `ingest/pipeline.py`.

```bash
cd backend
.venv/bin/python -m app.ingest.pipeline --reset   # 12 seed docs -> 550 chunks
.venv/bin/python -m app.ingest.pipeline --all-banking   # (later) ingest all 197 banking docs
```

**Result:** 12 files → **550 chunks**, 0 errors, ~5s (model cached).
Sanity retrieval returns the correct authority per query (RBI / NPCI / BANK) with scores 0.77–0.85.

## Acceptance
- [x] Registry prints counts by domain/authority; API filters work; 404 on unknown id.
- [x] Pipeline report `total_chunks > 500` (550); `VectorStore.count() == 550`; `errors == []`.
- [x] Every chunk carries `source_id, domain, authority, institution, is_authoritative`.
- [x] Tests: `pytest` → 16 passed (discover rules, chunk split/heading/merge, PDF + HTML-as-PDF recovery).

## Decisions / gotchas (RCA)
- **Embeddings via ChromaDB ONNX `all-MiniLM-L6-v2`, not sentence-transformers.**
  torch download broke on a flaky network; ONNX is the same model, ~80MB, no torch.
  sentence-transformers remains an opt-in upgrade (`pip install` + it's auto-detected).
- **`DetachedInstanceError` after commit** → fixed with `expire_on_commit=False`
  in the upsert session (SQLAlchemy expires objects on commit by default).
- **3 of 20 "PDF" files are actually HTML** (RBI blocked downloads → error pages saved
  as `.pdf`). The loader now **sniffs magic bytes** and routes them through the HTML
  path, so their content is recovered instead of silently dropped.
- **Chunk size 384 tokens** (down from 512): finer chunks retrieve more precisely for
  FAQ/clause text and cleared the >500 bar. Tunable via `CHUNK_TARGET_TOKENS` env.
- **Dependencies frozen** to `requirements.txt` (curated) + `requirements.lock.txt` (full).
