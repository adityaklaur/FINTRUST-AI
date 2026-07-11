# Phase 9 — React Frontend ✅

**Goal:** a polished, functional UI over the backend API.

## Stack
React 18 + TypeScript + Vite 6 + **Tailwind CSS v4** (via `@tailwindcss/vite`) +
`@tanstack/react-query` + axios. Hand-written components (shadcn/ui generator
skipped to avoid setup churn; the aesthetic is matched with Tailwind directly).

## What was built (`frontend/src/`)
- `api/client.ts`, `api/types.ts` — axios instance + TS mirrors of backend schemas.
- `hooks/useAskQuery.ts` (mutation → `POST /api/query`), `hooks/useAudit.ts` (query → `GET /api/audit`).
- `components/` — QueryPanel, AnswerPanel, CitationCard, RiskBadge, CategoryBadge,
  EscalationRoute, EvidenceChecklist, DisclaimerBanner.
- `pages/` — Home (query + results, debug accordion), AuditHistory (filter + expandable
  rows), SourceExplorer (filter + authority badges), EvalDashboard (metric cards + run button).
- `App.tsx` — tab nav + layout; `main.tsx` — react-query provider.
- `vite.config.ts` — `/api` proxy to the backend (container-aware via `VITE_PROXY_TARGET`).

## Verified
- [x] `npm run build` → `tsc` clean + Vite bundle (141 modules, ~83 kB gzip JS).
- [x] Dev server serves the app on :5173.
- [x] `/api/*` proxies to the backend (health + query confirmed through :5173).
- [ ] Vitest hook test — **deferred** (build + live e2e already prove the UI wiring;
      adding Vitest means more dev-deps over the slow public registry). Optional follow-up.

## npm gotcha (important)
Global npm points at a private **AWS CodeArtifact** registry that needs an auth
token and hangs without it. `frontend/.npmrc` pins this project to public npm so
`npm install` works regardless. To use CodeArtifact instead: `aws codeartifact
login --tool npm …` and delete `frontend/.npmrc`.
