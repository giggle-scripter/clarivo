from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.exercise import ExerciseDetailResponse, ExerciseResponse
from app.services.exercise_service import get_exercise, list_exercises


router = APIRouter(prefix="/exercises", tags=["exercises"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[ExerciseResponse])
def read_exercises(db: DatabaseSession) -> list[ExerciseResponse]:
    return list(list_exercises(db))


@router.get("/{exercise_id}", response_model=ExerciseDetailResponse)
def read_exercise(exercise_id: UUID, db: DatabaseSession) -> ExerciseDetailResponse:
    exercise = get_exercise(db, exercise_id)
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        )
    return exercise
