from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


if TYPE_CHECKING:
    from app.db.models.prompt import Prompt


class ExerciseType(StrEnum):
    DAILY_60 = "DAILY_60"
    OPINION = "OPINION"
    INTERVIEW = "INTERVIEW"
    TECHNICAL_EXPLANATION = "TECHNICAL_EXPLANATION"
    STORYTELLING = "STORYTELLING"
    SUMMARY = "SUMMARY"


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, default="")
    exercise_type: Mapped[ExerciseType] = mapped_column(
        Enum(ExerciseType, name="exercise_type", native_enum=False),
        index=True,
    )
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    prep_seconds: Mapped[int] = mapped_column(Integer, default=15)
    speak_seconds: Mapped[int] = mapped_column(Integer, default=60)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    prompts: Mapped[list["Prompt"]] = relationship(
        back_populates="exercise",
        cascade="all, delete-orphan",
        order_by="Prompt.created_at",
    )
