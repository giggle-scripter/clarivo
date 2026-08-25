# Clarivo

Clarivo is an AI articulation coach initially focused on spoken Vietnamese.

## Problem

Clarivo helps people express ideas more clearly, concisely, and coherently. The
first version focuses on common speaking problems such as late main points,
repetition, fillers, weak structure, and answers that drift away from the prompt.

## Core loop

```text
Prompt
→ Speak
→ Analyze
→ Feedback
→ Retry
```

## Current status

Phase 2 — Recording. Clarivo now supports the practice-selection flow, creates
sessions and retry attempts, records audio in the browser, stores it in MinIO,
and reloads it for playback. ASR and analysis are the next product phase.

## Stack

- Next.js and TypeScript for the web application
- FastAPI for the API
- PostgreSQL for persistent data
- SQLAlchemy and Alembic for database access and migrations

## Repository boundaries

```text
apps/          Product applications
ai/            Speech and language analysis modules
data/          Dataset metadata and reproducible data instructions
experiments/   Research notebooks and experimental results
scripts/       Development, data, and evaluation utilities
docs/          Product and engineering specifications
```

The original planning documents are retained in `instruction_docs/`.

## Local development

Copy `.env.example` to `.env`, install backend dependencies, then start
PostgreSQL:

```bash
uv sync --project apps/api --dev
docker compose up -d
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
uv run --project apps/api python scripts/seed_prompts.py
uv run --project apps/api uvicorn app.main:app --app-dir apps/api --reload
npm install --prefix apps/web
npm run dev --prefix apps/web
```

Run backend tests with:

```bash
uv run --project apps/api pytest apps/api/tests
```

Frontend setup instructions will be added when that application is initialized.

## Roadmap

The first vertical slice is:

```text
Home
→ Exercise list
→ Select prompt
→ Create session
```

See `instruction_docs/clarivo_roadmap.md` for the complete product roadmap.
