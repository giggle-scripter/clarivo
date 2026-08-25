from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_storage_service
from app.core.config import settings
from app.db.models import AttemptStatus
from app.schemas.attempt import AttemptResponse
from app.services.attempt_service import MIME_EXTENSIONS, attach_audio
from app.services.session_service import get_attempt
from app.services.storage_service import StorageService


router = APIRouter(prefix="/attempts", tags=["attempts"])
DatabaseSession = Annotated[Session, Depends(get_db)]
ObjectStorage = Annotated[StorageService, Depends(get_storage_service)]


@router.get("/{attempt_id}", response_model=AttemptResponse)
def read_attempt(attempt_id: UUID, db: DatabaseSession) -> AttemptResponse:
    attempt = get_attempt(db, attempt_id)
    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )
    return attempt


@router.post("/{attempt_id}/audio", response_model=AttemptResponse)
def upload_attempt_audio(
    attempt_id: UUID,
    db: DatabaseSession,
    storage: ObjectStorage,
    audio: Annotated[UploadFile, File()],
    duration_ms: Annotated[int, Form(ge=250, le=300_000)],
) -> AttemptResponse:
    attempt = get_attempt(db, attempt_id)
    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )
    if attempt.status == AttemptStatus.UPLOADED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attempt audio has already been uploaded",
        )
    if audio.content_type not in MIME_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported audio format",
        )
    if audio.size is not None and audio.size > settings.max_audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Audio file is too large",
        )
    return attach_audio(
        db,
        storage,
        attempt=attempt,
        audio=audio,
        duration_ms=duration_ms,
    )


@router.get("/{attempt_id}/audio", response_class=StreamingResponse)
def stream_attempt_audio(
    attempt_id: UUID,
    db: DatabaseSession,
    storage: ObjectStorage,
) -> StreamingResponse:
    attempt = get_attempt(db, attempt_id)
    if attempt is None or attempt.audio_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt audio not found",
        )
    stored_audio = storage.get_audio(attempt.audio_url)

    def stream_chunks():
        try:
            while chunk := stored_audio.body.read(64 * 1024):
                yield chunk
        finally:
            stored_audio.body.close()

    return StreamingResponse(
        stream_chunks(),
        media_type=stored_audio.content_type,
        headers={
            "Content-Length": str(stored_audio.content_length),
            "Cache-Control": "no-store",
        },
    )
