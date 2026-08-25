from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


if TYPE_CHECKING:
    from app.db.models.practice_session import PracticeSession


class AttemptStatus(StrEnum):
    CREATED = "CREATED"
    UPLOADED = "UPLOADED"


class Attempt(Base):
    __tablename__ = "attempts"
    __table_args__ = (
        UniqueConstraint(
            "practice_session_id",
            "attempt_number",
            name="uq_attempts_session_number",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    practice_session_id: Mapped[UUID] = mapped_column(
        ForeignKey("practice_sessions.id", ondelete="CASCADE"),
        index=True,
    )
    attempt_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[AttemptStatus] = mapped_column(
        Enum(AttemptStatus, name="attempt_status", native_enum=False),
        default=AttemptStatus.CREATED,
        index=True,
    )
    audio_url: Mapped[str | None] = mapped_column(String(1024))
    audio_duration_ms: Mapped[int | None] = mapped_column(Integer)
    audio_mime_type: Mapped[str | None] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    practice_session: Mapped["PracticeSession"] = relationship(
        back_populates="attempts"
    )
