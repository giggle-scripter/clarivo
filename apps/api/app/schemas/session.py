from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.practice_session import PracticeSessionStatus
from app.schemas.attempt import AttemptResponse
from app.schemas.exercise import PromptResponse


class PracticeSessionCreate(BaseModel):
    prompt_id: UUID
    user_id: UUID | None = None


class PracticeSessionResponse(BaseModel):
    id: UUID
    user_id: UUID | None
    exercise_id: UUID
    prompt_id: UUID
    status: PracticeSessionStatus
    started_at: datetime
    completed_at: datetime | None
    prompt: PromptResponse
    attempts: list[AttemptResponse]

    model_config = ConfigDict(from_attributes=True)
