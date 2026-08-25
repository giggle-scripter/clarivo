from pathlib import PurePosixPath
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.models import Attempt, AttemptStatus
from app.services.storage_service import StorageService


MIME_EXTENSIONS = {
    "audio/webm": ".webm",
    "audio/ogg": ".ogg",
    "audio/mp4": ".m4a",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
}


def attach_audio(
    db: Session,
    storage: StorageService,
    *,
    attempt: Attempt,
    audio: UploadFile,
    duration_ms: int,
) -> Attempt:
    content_type = audio.content_type or "application/octet-stream"
    extension = MIME_EXTENSIONS[content_type]
    object_key = str(
        PurePosixPath(str(attempt.practice_session_id))
        / f"{attempt.id}{extension}"
    )
    attempt.audio_url = storage.put_audio(
        object_key=object_key,
        file=audio.file,
        content_type=content_type,
    )
    attempt.audio_duration_ms = duration_ms
    attempt.audio_mime_type = content_type
    attempt.status = AttemptStatus.UPLOADED
    db.commit()
    db.refresh(attempt)
    return attempt


def find_attempt(db: Session, attempt_id: UUID) -> Attempt | None:
    return db.get(Attempt, attempt_id)
