from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Attempt, PracticeSession, Prompt, User


def _session_query():
    return select(PracticeSession).options(
        selectinload(PracticeSession.prompt),
        selectinload(PracticeSession.attempts),
    )


def create_practice_session(
    db: Session,
    *,
    prompt_id: UUID,
    user_id: UUID | None = None,
) -> PracticeSession | None:
    prompt = db.get(Prompt, prompt_id)
    if prompt is None or not prompt.is_active:
        return None
    if user_id is not None and db.get(User, user_id) is None:
        return None

    practice_session = PracticeSession(
        user_id=user_id,
        exercise_id=prompt.exercise_id,
        prompt_id=prompt.id,
    )
    db.add(practice_session)
    db.commit()
    return get_practice_session(db, practice_session.id)


def get_practice_session(
    db: Session,
    session_id: UUID,
) -> PracticeSession | None:
    return db.scalar(_session_query().where(PracticeSession.id == session_id))


def create_attempt(db: Session, session_id: UUID) -> Attempt | None:
    practice_session = db.get(PracticeSession, session_id)
    if practice_session is None:
        return None

    last_attempt_number = db.scalar(
        select(func.max(Attempt.attempt_number)).where(
            Attempt.practice_session_id == session_id
        )
    )
    attempt = Attempt(
        practice_session_id=session_id,
        attempt_number=(last_attempt_number or 0) + 1,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def get_attempt(db: Session, attempt_id: UUID) -> Attempt | None:
    return db.get(Attempt, attempt_id)
