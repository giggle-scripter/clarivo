from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


if TYPE_CHECKING:
    from app.db.models.attempt import Attempt
    from app.db.models.exercise import Exercise
    from app.db.models.prompt import Prompt
    from app.db.models.user import User


class PracticeSessionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    exercise_id: Mapped[UUID] = mapped_column(
        ForeignKey("exercises.id", ondelete="RESTRICT"),
        index=True,
    )
    prompt_id: Mapped[UUID] = mapped_column(
        ForeignKey("prompts.id", ondelete="RESTRICT"),
        index=True,
    )
    status: Mapped[PracticeSessionStatus] = mapped_column(
        Enum(
            PracticeSessionStatus,
            name="practice_session_status",
            native_enum=False,
        ),
        default=PracticeSessionStatus.ACTIVE,
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User | None"] = relationship(back_populates="practice_sessions")
    exercise: Mapped["Exercise"] = relationship()
    prompt: Mapped["Prompt"] = relationship()
    attempts: Mapped[list["Attempt"]] = relationship(
        back_populates="practice_session",
        cascade="all, delete-orphan",
        order_by="Attempt.attempt_number",
    )
