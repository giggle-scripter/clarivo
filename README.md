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

Phase 1 — Application foundation. The repository currently contains the initial
project boundaries and specifications; application scaffolding comes next.

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

Copy `.env.example` to `.env`, then start PostgreSQL:

```bash
docker compose up -d db
```

Backend and frontend setup instructions will be added when those applications
are initialized.

## Roadmap

The first vertical slice is:

```text
Home
→ Exercise list
→ Select prompt
→ Create session
```

See `instruction_docs/clarivo_roadmap.md` for the complete product roadmap.
