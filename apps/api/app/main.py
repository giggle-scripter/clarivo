from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import attempts, exercises, health, sessions
from app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="API for the Clarivo spoken-articulation coach.",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.web_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health.router)
    application.include_router(exercises.router)
    application.include_router(sessions.router)
    application.include_router(attempts.router)
    return application


app = create_app()
