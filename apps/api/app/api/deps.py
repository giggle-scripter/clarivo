from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings
from app.services.storage_service import StorageService


storage_service = StorageService(settings)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_storage_service() -> StorageService:
    return storage_service
