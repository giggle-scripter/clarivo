# Clarivo API

FastAPI backend for Clarivo.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL 17 (provided by the root Docker Compose file)

## Setup

From the repository root:

```bash
uv sync --project apps/api --dev
docker compose up -d db
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
uv run --project apps/api python scripts/seed_prompts.py
uv run --project apps/api uvicorn app.main:app --app-dir apps/api --reload
```

The API is then available at `http://localhost:8000`. Interactive documentation
is available at `/docs`.

## Tests

```bash
uv run --project apps/api pytest apps/api/tests
```

Tests use an isolated in-memory SQLite database and do not require Docker.
