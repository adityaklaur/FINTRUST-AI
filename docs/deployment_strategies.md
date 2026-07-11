# FinTrust AI Deployment Strategies: Free / Near-Free First

Last updated: 2026-07-11

This document explains where and how to deploy FinTrust AI with little or no money for a college/interview/portfolio showcase. It focuses on free and near-free options first, then gives a paid AWS fallback if you want a more serious deployment later.

FinTrust AI stack today:

- Frontend: React 18 + TypeScript + Vite + Tailwind
- Backend: FastAPI
- Relational storage: SQLite via SQLModel
- Vector store: local ChromaDB under `backend/data/vector_store`
- Default LLM mode: `LLM_PROVIDER=none` extractive/cited answers
- Optional LLM providers: Groq, Gemini, OpenAI, Anthropic
- Docker Compose exists and runs backend + frontend



## Short Answer: Best Strategy For Your Budget

Recommended free-first deployment:

> Deploy the React frontend on **Cloudflare Pages** or **Vercel**, and deploy the FastAPI backend on **Render Free** or **Koyeb Free**. Keep `LLM_PROVIDER=none` first, then add a free **Gemini** or **Groq** API key.

Why this is best for you:

- You want the lowest cost for friends/interviewers.
- You do not have much traffic.
- You already have a working React + FastAPI app.
- You do not need Kubernetes/Jenkins/RDS/API Gateway.
- Your app can run in `LLM_PROVIDER=none` mode with no API cost.
- Gemini/Groq free tiers are enough for occasional demo usage.

Recommended path:

1. **Frontend:** Cloudflare Pages or Vercel free tier.
2. **Backend:** Render Free or Koyeb Free.
3. **Database/vector store:** keep prebuilt `backend/data` for demo; do not add Postgres yet.
4. **LLM:** start offline (`LLM_PROVIDER=none`), then add Gemini/Groq free API.
5. **If free hosting becomes unreliable:** move backend to Railway Hobby (`$5/month`) or AWS EC2.

Expected cost:

- Fully free showcase: `$0/month`, but cold starts and no persistent backend writes.
- More reliable hobby deployment: `$5-$10/month`.
- AWS EC2 serious deployment: roughly `$10-$25/month` without RDS.

## The Big Constraint: SQLite + Chroma Persistence

FinTrust currently stores:

- SQLite audit/source registry in `backend/data/fintrust.db`
- Chroma vector store in `backend/data/vector_store`

Free hosting platforms often have **ephemeral filesystems**, meaning files written after deploy can disappear when the service restarts.

This gives two deployment modes:

### Mode A: Free showcase mode

Use prebuilt registry/vector store committed or bundled into the deployed image. Treat audit logs as temporary.

Good for:

- friends
- interviewers
- professors
- demos

Not good for:

- real users
- important persistent audit logs
- production claims history

### Mode B: Persistent mode

Use a server or paid persistent volume.

Good options:

- AWS EC2 with EBS
- Railway with volume/Postgres
- Fly.io with volume
- Render paid disk
- Supabase/Neon Postgres later for relational data

For your first public demo, Mode A is acceptable if you clearly understand the limitation.

## Recommended Free / Near-Free Architectures

### Option 1 — Best $0 Beginner Deployment

```text
Cloudflare Pages or Vercel  -> React frontend
Render Free or Koyeb Free   -> FastAPI backend
Bundled backend/data        -> Chroma + SQLite seed data
Gemini/Groq free API        -> optional LLM prose
```

Pros:

- `$0/month`
- easiest to share public URLs
- simple GitHub-based deployment
- enough for interview demos

Cons:

- backend sleeps/cold starts
- persistent audit logs are not reliable
- local Chroma changes may reset after redeploy/restart
- free Postgres options have limits or expiry

Best use:

- first public demo
- portfolio link
- short-term showcase

### Option 2 — Best Near-Free Reliable Deployment

```text
Cloudflare Pages/Vercel frontend
Railway Hobby backend
Railway volume or Neon/Supabase later
Gemini/Groq free API
```

Cost:

- about `$5/month` minimum for Railway Hobby
- small overage possible

Pros:

- much less cold-start pain
- easier than AWS
- good developer experience
- more reliable than fully free hosting

Cons:

- not truly free
- usage-based billing needs monitoring

Best use:

- you want reliability for a month or more
- interviewer link should open quickly

### Option 3 — Best Serious Low-Cost Deployment

```text
AWS EC2 t4g.small/t3.small
Docker Compose
Caddy HTTPS
Persistent backend/data on EBS
Gemini/Groq API
```

Cost:

- often around `$10-$25/month`
- can be covered by AWS credits if eligible

Pros:

- looks professional
- persistent disk
- full control
- good learning value
- easy to explain in interviews

Cons:

- you manage the server
- needs AWS budget alerts
- not as simple as Render/Vercel

Best use:

- after the free demo works
- when you want a stable 1-year project URL

### Option 4 — Oracle Cloud Always Free VPS

Oracle Cloud Always Free can be attractive because it offers always-free compute, including Ampere ARM resources. Current public docs show a reduced Always Free Ampere allowance around 2 OCPUs and 12 GB RAM for Always Free tenancies, plus block storage limits.

Pros:

- potentially free for long-term VPS hosting
- enough RAM for your app if you can get capacity
- persistent VM style deployment

Cons:

- account creation/capacity can be painful
- ARM compatibility must be checked
- free tier policy has changed before
- support/community experiences are mixed

Best use:

- if you can get an Oracle free VM reliably
- if you want long-term free VPS and can tolerate setup friction

I would not make Oracle the first choice, but it is worth trying in parallel.

## Platform Comparison For FinTrust

| Platform | Monthly cost | Good for | Main problem | Recommendation |
|---|---:|---|---|---|
| Cloudflare Pages | Free | React frontend | frontend only | Excellent frontend host |
| Vercel Hobby | Free | React frontend, light serverless | FastAPI bundle/persistence not ideal | Great frontend host |
| Render Free | Free | FastAPI backend demo | sleeps, no persistent disk on free, free DB expiry | Best beginner backend |
| Koyeb Free | Free | one Docker/FastAPI service | 512 MB RAM, no volumes, sleeps after 1 hour | Good backend alternative |
| Hugging Face Spaces | Free | AI demos, Docker demos | stateless unless paid storage | Good if demo is AI-first |
| Railway Hobby | ~$5/mo | reliable hobby app | not fully free | Best cheap reliability |
| Fly.io | $0-$10+ | Docker, volumes, global | more complex, IPv4/volume costs | Good if comfortable |
| AWS EC2 | ~$10-$25 | serious deployment | server management | Best professional fallback |
| Supabase | Free/paid | Auth + Postgres | not backend hosting; Chroma separate | Add later for auth/db |
| Neon | Free/paid | Postgres | scale-to-zero; not backend hosting | Add later for Postgres |

## Recommended Free Deployment Plan

### Step 1: Freeze a showcase build

Before deploying, run:

```bash
cd backend
.venv/bin/python -m pytest
.venv/bin/ruff check app tests
.venv/bin/python -m app.evaluation.runner

cd ../frontend
npm run build
```

### Step 2: Decide whether audit logs must persist

For portfolio demo:

- okay if audit logs are temporary
- okay if SQLite/Chroma are bundled and reset on redeploy

For real product:

- need persistent volume or Postgres

### Step 3: Deploy frontend free

Best: Cloudflare Pages or Vercel.

Cloudflare Pages:

- free
- unlimited static requests/bandwidth on free plan
- 500 builds/month
- good with custom domains

Vercel:

- free Hobby plan
- great React/Vite developer experience
- good preview deployments
- non-commercial/personal usage

Recommended frontend:

```text
Cloudflare Pages if you want durable free hosting.
Vercel if you want easiest GitHub UX.
```

Frontend environment:

```env
VITE_API_URL=https://your-backend-url
```

### Step 4: Deploy backend free

Option A: Render Free

- easiest
- supports Python/FastAPI
- free web service
- sleeps after inactivity
- no persistent local filesystem on free

Backend command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Build command:

```bash
pip install -r requirements.txt
```

Option B: Koyeb Free

- one free web service
- Docker-friendly
- 512 MB RAM
- no volumes
- scales to zero after one hour

Good if Render memory/cold start is annoying.

Option C: Hugging Face Spaces Docker

- free AI-demo hosting
- good for showcasing AI apps
- port 7860
- filesystem is not persistent unless paid storage bucket

Good if you want your app to look like an AI demo.

### Step 5: Configure backend environment

Safe free mode:

```env
APP_ENV=production
LLM_PROVIDER=none
LLM_API_KEY=
LLM_MODEL=
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend-url
```

Optional free LLM:

```env
LLM_PROVIDER=gemini
LLM_API_KEY=your_key
```

or

```env
LLM_PROVIDER=groq
LLM_API_KEY=your_key
```

### Step 6: Make Chroma/SQLite work on free backend

For free platforms with ephemeral disk:

Option A:

- include built `backend/data` in deploy image/repo
- treat it as read-mostly
- audit logs may reset

Option B:

- rebuild registry + ingestion at startup
- slower cold starts
- not ideal if memory is low

Option C:

- use paid/persistent disk
- best long-term

For free demo, use Option A.

## LLM API Free / Cheap Strategy

### Best first choice: `LLM_PROVIDER=none`

Pros:

- free forever
- no rate limits
- no API failures
- citations remain strong

Cons:

- answer prose is less fluent

Use for:

- base demo
- deployment reliability

### Best free hosted LLM: Gemini

Pros:

- Google AI Studio free tier
- good quality
- long context
- easy key setup

Cons:

- free quota varies by model/project
- sometimes rate-limited

Use for:

- best free general answer quality

### Fastest free hosted LLM: Groq

Pros:

- very fast
- no card for free tier
- good open models

Cons:

- token-per-minute limits can bite
- model catalog changes

Use for:

- low-latency demo
- short answers

### OpenRouter

Pros:

- one key for many models
- free models available
- useful fallback

Cons:

- free daily request cap can be low
- free models change

Use for:

- experimentation

### OpenAI / Anthropic API

Pros:

- stable high quality

Cons:

- paid API even if you have ChatGPT/Claude subscription
- web subscription is usually separate from API billing

Use for:

- final polished demo if you are willing to spend small amount

## Supabase / Neon Strategy

Do not add Supabase just because it is popular.

Add Supabase if you need:

- login
- user profiles
- saved chats
- hosted Postgres
- auth UI

Supabase free plan can be enough for:

- auth
- small Postgres tables
- audit logs

But Supabase does not replace:

- FastAPI backend
- ChromaDB vector store

Neon is a good free Postgres alternative:

- 0.5 GB storage per project
- scale-to-zero
- good for audit/source registry later

For first deployment:

- keep SQLite
- move to Supabase/Neon only after public demo works

## Best 1-Year Low-Cost Plan

If you want something working for a year:

### Month 1: Free

- Frontend: Cloudflare Pages or Vercel
- Backend: Render Free or Koyeb Free
- LLM: none + Gemini/Groq testing
- DB/vector: bundled `backend/data`

### Month 2-12: Cheap reliable

If free backend cold starts or resets are annoying:

- Move backend to Railway Hobby (~$5/month) or AWS EC2.
- Keep frontend on Cloudflare/Vercel free.
- Keep LLM mostly Gemini/Groq free.
- Add domain if needed.

Expected yearly cost:

- fully free if you tolerate limitations
- around `$60/year` with Railway Hobby backend
- around `$120-$250/year` with AWS EC2 + domain/storage

## What I Recommend You Actually Do

Recommended path:

1. Deploy frontend to Cloudflare Pages.
2. Deploy backend to Render Free first.
3. Use `LLM_PROVIDER=none`.
4. Add Gemini API key.
5. Test with friends/interviewers.
6. If cold starts are embarrassing, move backend to Railway Hobby or AWS EC2.

This gives you:

- fastest launch
- almost zero cost
- public links
- enough polish for interviews
- no unnecessary DevOps

## Claude Prompt: Free Deployment Preparation

Paste this to Claude:

```text
You are helping deploy the existing FinTrust AI app on free or near-free platforms.

Project root:
FINTRUST-AI/

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

Goal:
Prepare the app for a free/near-free showcase deployment:
- frontend on Cloudflare Pages or Vercel
- backend on Render Free or Koyeb Free
- LLM_PROVIDER=none by default
- optional Gemini/Groq keys
- no Postgres/RDS initially
- no Kubernetes/Jenkins/API Gateway

Tasks:
1. Inspect current backend and frontend build setup.
2. Verify frontend can use VITE_API_URL for deployed backend URL.
3. Verify backend supports CORS_ORIGINS from env.
4. Add frontend/.env.example if missing.
5. Add Render deploy notes or render.yaml if appropriate.
6. Add Koyeb deploy notes if useful.
7. Add Cloudflare Pages / Vercel frontend deploy notes.
8. Explain how backend/data persistence works on free platforms.
9. Ensure no API keys are committed.

Acceptance criteria:
- npm run build passes.
- backend pytest passes.
- docs include step-by-step free deployment instructions.
- app still works locally.
- no secrets are printed or committed.
```

## Final Recommendation

Use this stack first:

```text
Frontend: Cloudflare Pages or Vercel Free
Backend: Render Free
LLM: none first, then Gemini/Groq free key
Database/vector: bundled backend/data for showcase
Upgrade path: Railway Hobby or AWS EC2 if cold starts/persistence become a problem
```

This is the best balance of:

- free cost
- low setup time
- public shareable demo
- enough seriousness for interviews
- no unnecessary infrastructure complexity



## Do You Need Kubernetes, Jenkins, CDN, API Gateway?

For your current project: no.


| Tool          | Needed Now?   | Why                                                                                                    |
| ------------- | ------------- | ------------------------------------------------------------------------------------------------------ |
| Kubernetes    | No            | Too complex for a single FastAPI + React + local Chroma app. Use Docker Compose.                       |
| Jenkins       | No            | GitHub Actions is simpler if you need CI/CD. Manual deploy is enough first.                            |
| API Gateway   | No            | FastAPI behind Caddy/Nginx is enough. API Gateway is useful for Lambda/serverless/microservices later. |
| CDN           | Not required  | Vite static frontend is small. Add CloudFront/Cloudflare later if you want custom domain/performance.  |
| RDS           | Not initially | SQLite works for demo. Use Postgres/RDS only when multi-user writes matter.                            |
| ECS/Fargate   | Not initially | More production-like but more setup/cost. EC2 is easier for first deployment.                          |
| S3            | Optional      | Useful later for source uploads, user files, backups. Not required for MVP.                            |
| Load Balancer | No            | One EC2 instance is fine for friends/interviewers.                                                     |




## Free Credits And Student Offers



### AWS

AWS changed the Free Tier for newer customers.

Current public AWS docs say new customers who create accounts after July 15, 2025 can get `$100` credits on sign-up and can earn up to another `$100` by completing AWS onboarding activities. Free account plans are for experiments/proofs of concept and expire after six months or when credits are used. Paid account plans allow broader service access and then bill normally after credits.

Practical meaning:

- You may get up to `$200` in AWS credits if you are a new eligible AWS customer.
- You should set AWS Budgets immediately.
- If you use Free account plan, check which services are allowed.
- If using EC2/RDS/Bedrock seriously, you may need paid plan with credits.

Useful for FinTrust:

- EC2
- EBS
- Route 53
- RDS later
- Bedrock testing later, not required now



### Azure

Azure free account typically provides `$200` credit for 30 days. Azure for Students can provide `$100` credit for 12 months with eligible student verification and no credit card.

Practical meaning:

- Azure is good if your college email qualifies.
- Azure App Service + Azure Database for PostgreSQL is possible.
- For your current Docker Compose app, Azure is not simpler than EC2 unless you already know Azure.



### Google Cloud

Google Cloud free trial generally provides `$300` credit for 90 days for new customers. You are not charged unless you upgrade to a paid account.

Practical meaning:

- Good credits.
- Cloud Run is attractive for containerized APIs.
- But local Chroma/SQLite persistence needs care.
- You may need Cloud SQL or persistent storage decisions.



### Supabase

Supabase free tier is useful for:

- Postgres
- Auth
- file storage
- simple backend tables
- social login later

Supabase is not a complete replacement for your FastAPI + Chroma app.

Free tier public limits include roughly:

- 500 MB Postgres
- 50k monthly active users
- 1 GB file storage
- 2 active free projects
- free projects can pause after inactivity

Use Supabase if:

- you want login/auth quickly
- you want hosted Postgres without managing RDS
- you later migrate SQLite audit/source registry to Postgres

Do not use Supabase first if:

- you want the fastest deployment of the current app
- you do not need login yet
- you want local ChromaDB unchanged



## Deployment Options Compared



### Option A — Recommended: AWS EC2 + Docker Compose

Best for your case.

Architecture:

```text
User Browser
  |
  v
Domain / HTTPS
  |
  v
Caddy or Nginx on EC2
  |--------------------------|
  v                          v
React frontend container     FastAPI backend container
                             |
                             v
                      backend/data/
                      SQLite + ChromaDB
```

Services:

- EC2 instance
- EBS disk
- Security group
- Elastic IP
- Optional Route 53 domain
- Optional CloudWatch logs

Pros:

- Cheapest serious deployment.
- Full control.
- Docker Compose works directly.
- Persistent local ChromaDB is easy.
- Looks good for interview explanation.
- Easy to later migrate to RDS/Postgres/S3/ECS.

Cons:

- You manage server updates.
- You must secure SSH and firewall.
- If EC2 dies and no backups exist, data is lost.

Estimated monthly cost:

- EC2 `t4g.small`: roughly `$8-$15/month` depending region/pricing.
- EBS 20-30 GB: a few dollars/month.
- Domain: about `$10-$15/year`.
- Total for demo: likely `$10-$25/month`.

Use this if:

- you are okay with AWS
- you want portfolio-quality deployment
- traffic is low
- you want to learn real deployment



### Option B — Easiest PaaS: Render

Architecture:

```text
Render Static Site -> React frontend
Render Web Service -> FastAPI backend
Render Disk or DB? -> persistence issue
```

Pros:

- Very easy GitHub deploy.
- Free web service possible.
- React static site easy.
- Good first deployment if you hate server setup.

Cons:

- Free services sleep after inactivity.
- Free Postgres expires after 30 days.
- Free services do not preserve local filesystem changes.
- ChromaDB local persistence may not be safe unless using paid persistent disk.

Use Render if:

- you want a quick public URL.
- you can accept cold starts.
- you use paid persistent disk or rebuild Chroma at startup.



### Option C — Railway

Pros:

- Very developer-friendly.
- Fast deployments.
- Supports multi-service apps and Postgres.
- Good for demos.

Cons:

- Not permanently free in the same sense.
- Hobby plan has monthly minimum.
- Persistent volumes/databases add cost.

Use Railway if:

- you value speed and simplicity over lowest cost.
- `$5-$15/month` is acceptable.



### Option D — Supabase + Vercel/Netlify + Backend Elsewhere

Architecture:

```text
Vercel/Netlify -> React frontend
FastAPI backend -> EC2/Render/Railway/Fly
Supabase -> Auth + Postgres
Chroma -> still backend local or migrated later
```

Pros:

- Supabase Auth is excellent.
- Hosted Postgres is easy.
- Frontend deployment is very simple.
- Good if adding login soon.

Cons:

- Does not host your FastAPI backend by itself.
- Supabase Edge Functions are not ideal for this Python RAG backend.
- You still need backend hosting.
- ChromaDB remains a separate problem.

Use Supabase later for:

- user login
- saved chat history
- Postgres audit/source registry
- team/admin roles



### Option E — AWS Elastic Beanstalk

Pros:

- Managed EC2-style platform.
- Easier than raw ECS.
- Good for Python apps.

Cons:

- Less transparent than plain EC2.
- Frontend still needs static hosting or same container.
- Docker Compose multi-service setup can be awkward.

Use only if:

- you want managed AWS platform and do not want to SSH into EC2.



### Option F — AWS ECS/Fargate + RDS + S3 + CloudFront

Pros:

- More production-grade.
- Scalable.
- Good architecture for real customers.

Cons:

- More expensive.
- More moving parts.
- Harder for first deployment.
- Overkill for friends/interviewers.

Use later when:

- product has users.
- you need uptime and scaling.
- you have CI/CD and monitoring.



## Recommended Strategy For You



### Stage 0 — Local Demo Polish

Before cloud:

```bash
cd backend
.venv/bin/python -m pytest
.venv/bin/ruff check app tests
.venv/bin/python -m app.evaluation.runner

cd ../frontend
npm run build
```

Make sure:

- backend health works
- frontend build works
- evaluation report exists
- no API keys are committed



### Stage 1 — First Public Deployment

Use AWS EC2 + Docker Compose.

Recommended EC2:

- `t4g.small` if ARM Docker images/builds work
- `t3.small` if you want easier x86 compatibility
- Ubuntu 24.04
- 20-30 GB EBS

Why `small`, not `micro`:

- ChromaDB + FastAPI + React container can be memory-hungry.
- `micro` may work but can feel fragile.
- `small` gives 2 GB RAM.

Stage 1 should use:

- SQLite
- local Chroma
- `LLM_PROVIDER=none` or `groq` / `gemini`
- no RDS
- no Kubernetes



### Stage 2 — Add Domain + HTTPS

Use:

- Caddy for automatic HTTPS
- domain from Namecheap/Cloudflare/Route 53

Example:

- `https://fintrust.yourdomain.com`
- backend under `/api`
- frontend under `/`



### Stage 3 — Add Managed DB Later

Move from SQLite to Postgres when:

- multiple users
- login
- concurrent writes
- cloud persistence concerns

Options:

- Supabase Postgres
- Neon Postgres
- AWS RDS Postgres
- Railway Postgres

For Chroma:

- keep local Chroma first
- later migrate to Qdrant Cloud / pgvector / hosted vector DB if needed



## Step-By-Step AWS EC2 Deployment Plan



### 1. Prepare local repository

Checklist:

- `backend/.env.example` exists
- `frontend/.env.example` exists if needed
- `.gitignore` excludes `.env`, `.venv`, `node_modules`, cache
- Docker Compose works locally
- evaluation report works



### 2. Create AWS budget first

Before EC2:

- AWS Billing -> Budgets
- Create monthly budget: `$10` or `$20`
- Email alert at 50%, 80%, 100%

This is mandatory for first-time AWS usage.

### 3. Create EC2 instance

Recommended:

- Region: `ap-south-1` Mumbai or closest to you
- Instance: `t4g.small` or `t3.small`
- OS: Ubuntu 24.04
- Storage: 30 GB gp3
- Security group:
  - SSH 22 from your IP only
  - HTTP 80 from anywhere
  - HTTPS 443 from anywhere
  - Do not open 8000 or 5173 publicly



### 4. Install Docker on EC2

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
newgrp docker
docker --version
docker compose version
```



### 5. Upload or clone project

Option A: GitHub private repo:

```bash
git clone <your-private-repo-url> FINTRUST-AI
cd FINTRUST-AI
```

Option B: copy from local using `scp`:

```bash
scp -r \"FINTRUST-AI\" ubuntu@YOUR_EC2_IP:/home/ubuntu/
```



### 6. Create production env file

On EC2:

```bash
cd FINTRUST-AI/backend
cp .env.example .env
nano .env
```

Safe first deployment:

```env
APP_ENV=production
LLM_PROVIDER=none
LLM_API_KEY=
LLM_MODEL=
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-domain.com,http://YOUR_EC2_IP
```

If using Groq/Gemini:

```env
LLM_PROVIDER=groq
LLM_API_KEY=your_real_key_here
```

Never commit `.env`.

### 7. Run Docker Compose

```bash
cd ~/FINTRUST-AI
docker compose up --build -d
docker compose ps
docker compose logs -f backend
```

Check:

```bash
curl http://localhost:8000/api/health
```



### 8. Add Caddy reverse proxy

Install:

```bash
sudo apt install -y caddy
```

Example `/etc/caddy/Caddyfile`:

```caddy
your-domain.com {
    reverse_proxy /api/* localhost:8000
    reverse_proxy localhost:5173
}
```

If no domain yet, use EC2 IP for testing, but HTTPS is easier with a domain.

Restart:

```bash
sudo systemctl reload caddy
```



### 9. Persistence

Important:

Your current SQLite and Chroma paths live under:

```text
backend/data/
```

In Docker/EC2, make sure this folder persists. Your `docker-compose.yml` should mount it as a volume, for example:

```yaml
services:
  backend:
    volumes:
      - ./backend/data:/app/data
```

Ask Claude to verify the actual container path before changing it.

### 10. Backups

At minimum:

```bash
tar -czf fintrust-backup-$(date +%F).tar.gz backend/data
```

Later:

- upload backup to S3
- automate daily cron



## LLM API Strategy



### Recommended order

1. `LLM_PROVIDER=none`
  - Free, reliable, fully cited, enough for demo.
2. `LLM_PROVIDER=groq`
  - Fast free tier, good for fluent answers.
3. `LLM_PROVIDER=gemini`
  - Good free tier, strong quality.
4. `LLM_PROVIDER=openai`
  - Paid, stable.
5. `LLM_PROVIDER=anthropic`
  - Good quality, paid; since you already have Claude subscription, check whether API access is included separately. Chat subscription and API billing are usually separate.



### Important API note

Do not assume Claude subscription gives free Anthropic API calls. Usually:

- Claude web/app subscription is for chat UI.
- Anthropic API is billed separately from console/API keys.

Same idea for ChatGPT Plus/Pro vs OpenAI API.

## Database Strategy



### Now

Keep:

- SQLite
- ChromaDB local

Why:

- no login yet
- low user count
- easiest deployment
- no migration work



### Later

Move SQLite to Postgres when:

- user accounts
- multiple concurrent users
- persistent cloud DB desired

Options:


| Option            | Good For            | Notes                                      |
| ----------------- | ------------------- | ------------------------------------------ |
| Supabase Postgres | Auth + DB           | Great later if login matters               |
| Neon Postgres     | Serverless Postgres | Simple and generous free tier historically |
| AWS RDS Postgres  | AWS-native          | More expensive but professional            |
| Railway Postgres  | Simple PaaS         | Easy, paid usage                           |


Vector DB later:


| Option       | Good For                        | Notes               |
| ------------ | ------------------------------- | ------------------- |
| Chroma local | MVP                             | Already works       |
| Qdrant Cloud | Hosted vector search            | Good upgrade        |
| pgvector     | One DB for vectors + relational | More migration work |
| Pinecone     | Managed vector DB               | Paid, polished      |




## Supabase Option

Use Supabase later for:

- authentication
- user profiles
- saved conversations
- audit logs
- admin dashboard
- Postgres storage

Do not move to Supabase immediately unless you need login.

Why not now:

- current app already works with SQLite
- Chroma is local and not replaced by Supabase unless using pgvector
- auth adds complexity

Suggested future Supabase design:

```text
Supabase Auth -> user login
Supabase Postgres -> users, chats, audit logs
FastAPI -> RAG backend
Chroma/Qdrant -> vector search
React -> frontend
```



## Best Deployment Recommendation

For your current goal — impressive portfolio demo for friends/interviewers:

### Best path

```text
AWS EC2 + Docker Compose + Caddy + local SQLite/Chroma + optional Groq/Gemini key
```

Why:

- serious enough to discuss in interviews
- affordable
- simple enough to finish
- no unnecessary Kubernetes/Jenkins/API Gateway
- works with current app architecture



### Cheapest path

```text
Render free/static + backend free web service
```

But beware:

- backend sleeps
- local persistence not reliable on free tier
- free Postgres expires in 30 days



### Clean managed path

```text
Railway Hobby + Postgres later
```

Cost:

- usually `$5+ / month`
- easier than AWS



### Most cloud-professional later

```text
AWS ECS/Fargate + RDS + S3 + CloudFront + Route53
```

Do this only after MVP has users.

## Claude Deployment Prompt

Paste this into Claude when you are ready for deployment prep:

```text
You are helping deploy the existing FinTrust AI project.

Project root:
FINTRUST-AI/

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

Goal:
Prepare the project for the recommended deployment path:
AWS EC2 + Docker Compose + Caddy/Nginx + persistent backend/data volume.

Do not deploy yet. Only prepare code/config/docs.

Tasks:
1. Inspect docker-compose.yml and Dockerfiles.
2. Verify backend data persistence for SQLite and Chroma under backend/data.
3. Add or update .dockerignore files.
4. Add production-safe environment variable examples.
5. Add CORS configuration for FRONTEND_URL / CORS_ORIGINS.
6. Add docs/DEPLOYMENT_CHECKLIST.md with exact EC2 steps.
7. Add a sample Caddyfile or Nginx config.
8. Add backup script for backend/data.
9. Ensure no API keys or secrets are committed.

Acceptance criteria:
- docker compose up --build works locally.
- backend /api/health works.
- frontend can call backend through /api.
- backend/data is persistent via volume.
- docs/DEPLOYMENT_CHECKLIST.md is beginner-friendly.
- no secrets are printed or committed.

After editing, list changed files and exact commands to verify.
```



## Deployment Checklist For First Time

Before deploying:

- [ ] Run backend tests.
- [ ] Run frontend build.
- [ ] Run evaluation.
- [ ] Confirm `LLM_PROVIDER=none` works.
- [ ] Confirm no secrets are committed.
- [ ] Confirm Docker Compose works locally.
- [ ] Create AWS budget.
- [ ] Choose EC2 instance.
- [ ] Configure security group.
- [ ] Add domain/HTTPS.
- [ ] Backup `backend/data`.



## Final Advice

Do not over-engineer deployment.

Your first successful public deployment should prove:

- the app works
- citations work
- retrieval works
- users can open it
- you understand the deployment architecture

It does not need Kubernetes, Jenkins, RDS, API Gateway, CloudFront or microservices yet.