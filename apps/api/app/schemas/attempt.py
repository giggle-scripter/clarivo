from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.attempt import AttemptStatus


class AttemptResponse(BaseModel):
    id: UUID
    practice_session_id: UUID
    attempt_number: int
    status: AttemptStatus
    audio_url: str | None
    audio_duration_ms: int | None
    audio_mime_type: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
