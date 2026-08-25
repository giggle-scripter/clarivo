from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.attempt import AttemptResponse
from app.schemas.session import PracticeSessionCreate, PracticeSessionResponse
from app.services.session_service import (
    create_attempt,
    create_practice_session,
    get_practice_session,
)


router = APIRouter(prefix="/practice-sessions", tags=["practice sessions"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=PracticeSessionResponse, status_code=201)
def start_practice_session(
    payload: PracticeSessionCreate,
    db: DatabaseSession,
) -> PracticeSessionResponse:
    practice_session = create_practice_session(
        db,
        prompt_id=payload.prompt_id,
        user_id=payload.user_id,
    )
    if practice_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt or user not found",
        )
    return practice_session


@router.get("/{session_id}", response_model=PracticeSessionResponse)
def read_practice_session(
    session_id: UUID,
    db: DatabaseSession,
) -> PracticeSessionResponse:
    practice_session = get_practice_session(db, session_id)
    if practice_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practice session not found",
        )
    return practice_session


@router.post(
    "/{session_id}/attempts",
    response_model=AttemptResponse,
    status_code=201,
)
def start_attempt(session_id: UUID, db: DatabaseSession) -> AttemptResponse:
    attempt = create_attempt(db, session_id)
    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practice session not found",
        )
    return attempt
