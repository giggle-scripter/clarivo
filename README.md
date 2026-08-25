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

Phase 1 — Application foundation. The FastAPI backend now includes health and
exercise read APIs, PostgreSQL models and migration for `Exercise` and `Prompt`,
plus an idempotent seed containing 18 Vietnamese practice prompts.

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
docker compose up -d db
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
uv run --project apps/api python scripts/seed_prompts.py
uv run --project apps/api uvicorn app.main:app --app-dir apps/api --reload
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
