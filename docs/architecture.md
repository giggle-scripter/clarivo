# Clarivo architecture

## System context

```text
Next.js web application
        ↓ HTTP
FastAPI application
        ├── PostgreSQL
        ├── Object storage (audio, later phase)
        └── AI modules
```

The initial architecture is a modular monorepo, not a set of microservices.

## Repository boundaries

- `apps/web`: product UI and browser-side recording flow.
- `apps/api`: HTTP contracts, application services, and persistence.
- `ai`: independently testable speech and language analysis.
- `data`: local datasets, metadata, and benchmark inputs.
- `experiments`: notebooks and research prototypes.
- `scripts`: reproducible setup, seeding, download, and evaluation tasks.
- `docs`: product and technical decisions.

## Backend layering

```text
Route
  ↓
Service
  ↓
Database or AI module
  ↓
Result
```

Routes handle HTTP concerns. Services contain business logic. SQLAlchemy models
represent persistence, while Pydantic schemas define API input and output.

AI algorithms stay outside route modules so they can be benchmarked without
running the web server.

## Initial deployment boundary

Docker Compose initially provisions PostgreSQL only. API, web, object storage,
and other infrastructure are added when their roadmap phase requires them.
