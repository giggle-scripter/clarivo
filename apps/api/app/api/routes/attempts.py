from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.attempt import AttemptResponse
from app.services.session_service import get_attempt


router = APIRouter(prefix="/attempts", tags=["attempts"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("/{attempt_id}", response_model=AttemptResponse)
def read_attempt(attempt_id: UUID, db: DatabaseSession) -> AttemptResponse:
    attempt = get_attempt(db, attempt_id)
    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )
    return attempt
