from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.exercise import ExerciseType


class PromptResponse(BaseModel):
    id: UUID
    exercise_id: UUID
    text: str
    topic: str
    target_skills: list[str]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExerciseResponse(BaseModel):
    id: UUID
    slug: str
    name: str
    description: str
    exercise_type: ExerciseType
    difficulty: int
    prep_seconds: int
    speak_seconds: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExerciseDetailResponse(ExerciseResponse):
    prompts: list[PromptResponse]
