from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models.exercise import Exercise
from app.db.models.prompt import Prompt


def list_exercises(db: Session) -> Sequence[Exercise]:
    statement = select(Exercise).order_by(Exercise.difficulty, Exercise.name)
    return db.scalars(statement).all()


def get_exercise(db: Session, exercise_id: UUID) -> Exercise | None:
    statement = (
        select(Exercise)
        .options(selectinload(Exercise.prompts.and_(Prompt.is_active.is_(True))))
        .where(Exercise.id == exercise_id)
    )
    return db.scalar(statement)
