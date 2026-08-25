"""Create exercises and prompts.

Revision ID: 20260825_0001
Revises:
Create Date: 2026-08-25
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260825_0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "exercises",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "exercise_type",
            sa.Enum(
                "DAILY_60",
                "OPINION",
                "INTERVIEW",
                "TECHNICAL_EXPLANATION",
                "STORYTELLING",
                "SUMMARY",
                name="exercise_type",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("difficulty", sa.Integer(), nullable=False),
        sa.Column("prep_seconds", sa.Integer(), nullable=False),
        sa.Column("speak_seconds", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_exercises_exercise_type", "exercises", ["exercise_type"])
    op.create_index("ix_exercises_slug", "exercises", ["slug"], unique=True)

    op.create_table(
        "prompts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("exercise_id", sa.Uuid(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("topic", sa.String(length=120), nullable=False),
        sa.Column(
            "target_skills",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercises.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "exercise_id",
            "text",
            name="uq_prompts_exercise_id_text",
        ),
    )
    op.create_index("ix_prompts_exercise_id", "prompts", ["exercise_id"])
    op.create_index("ix_prompts_is_active", "prompts", ["is_active"])


def downgrade() -> None:
    op.drop_index("ix_prompts_is_active", table_name="prompts")
    op.drop_index("ix_prompts_exercise_id", table_name="prompts")
    op.drop_table("prompts")
    op.drop_index("ix_exercises_slug", table_name="exercises")
    op.drop_index("ix_exercises_exercise_type", table_name="exercises")
    op.drop_table("exercises")
