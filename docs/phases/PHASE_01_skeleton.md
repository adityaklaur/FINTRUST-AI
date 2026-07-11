# Phase 1 — Project Skeleton ✅

**Goal:** running FastAPI backend with a health endpoint. No AI yet.

## What was built
```
backend/
  .venv/                 # Python 3.13 virtualenv (git-ignored)
  app/
    main.py              # FastAPI app, CORS, lifespan, router wiring
    api/health.py        # GET /api/health -> {status, version, timestamp}
    core/
      config.py          # pydantic-settings; all env knobs; path resolution
      constants.py       # APP_NAME, APP_VERSION, DISCLAIMER
      logging.py         # shared logging setup
  tests/test_health.py   # TestClient tests
  pytest.ini             # pythonpath=. so `app` imports in tests
  requirements.txt       # (frozen after Phase 3)
  .env.example           # documented, every value optional
  .gitignore
```

## How to run
```bash
cd "backend"
.venv/bin/python -m uvicorn app.main:app --reload --port 8000
# in another shell:
curl http://localhost:8000/api/health
```

## How to test
```bash
cd "backend"
.venv/bin/python -m pytest        # 2 passed
.venv/bin/ruff check app          # clean
```

## Acceptance criteria
- [x] `uvicorn app.main:app` starts without errors
- [x] `GET /api/health` → `{"status":"ok","version":"0.1.0",...}`
- [x] `pytest` → PASSED (2 tests)
- [x] `ruff check app` → clean
- [ ] React frontend — **deliberately deferred to Phase 9** (built once, against real endpoints, instead of a throwaway placeholder now)

## Notes
- Installed (Py 3.13): fastapi 0.139, pydantic 2.13, pydantic-settings 2.14,
  sqlmodel 0.0.39, uvicorn 0.51, pytest 9.1, httpx 0.28, ruff 0.15.
- Known warning: Starlette 1.3 flags `httpx`→`httpx2` for its TestClient. Harmless;
  revisit in Phase 10.
