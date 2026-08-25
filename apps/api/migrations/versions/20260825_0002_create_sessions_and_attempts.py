"""Create users, practice sessions, and attempts.

Revision ID: 20260825_0002
Revises: 20260825_0001
Create Date: 2026-08-25
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260825_0002"
down_revision: str | None = "20260825_0001"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "practice_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("exercise_id", sa.Uuid(), nullable=False),
        sa.Column("prompt_id", sa.Uuid(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "COMPLETED",
                name="practice_session_status",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercises.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompts.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_practice_sessions_exercise_id",
        "practice_sessions",
        ["exercise_id"],
    )
    op.create_index(
        "ix_practice_sessions_prompt_id",
        "practice_sessions",
        ["prompt_id"],
    )
    op.create_index(
        "ix_practice_sessions_status",
        "practice_sessions",
        ["status"],
    )
    op.create_index(
        "ix_practice_sessions_user_id",
        "practice_sessions",
        ["user_id"],
    )

    op.create_table(
        "attempts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("practice_session_id", sa.Uuid(), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "CREATED",
                "UPLOADED",
                name="attempt_status",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("audio_url", sa.String(length=1024), nullable=True),
        sa.Column("audio_duration_ms", sa.Integer(), nullable=True),
        sa.Column("audio_mime_type", sa.String(length=120), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["practice_session_id"],
            ["practice_sessions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "practice_session_id",
            "attempt_number",
            name="uq_attempts_session_number",
        ),
    )
    op.create_index(
        "ix_attempts_practice_session_id",
        "attempts",
        ["practice_session_id"],
    )
    op.create_index("ix_attempts_status", "attempts", ["status"])


def downgrade() -> None:
    op.drop_index("ix_attempts_status", table_name="attempts")
    op.drop_index("ix_attempts_practice_session_id", table_name="attempts")
    op.drop_table("attempts")
    op.drop_index("ix_practice_sessions_user_id", table_name="practice_sessions")
    op.drop_index("ix_practice_sessions_status", table_name="practice_sessions")
    op.drop_index("ix_practice_sessions_prompt_id", table_name="practice_sessions")
    op.drop_index("ix_practice_sessions_exercise_id", table_name="practice_sessions")
    op.drop_table("practice_sessions")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
