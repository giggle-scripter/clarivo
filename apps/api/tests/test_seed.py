from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Exercise, Prompt
from app.db.seed import seed_prompts


def test_seed_prompts_is_idempotent(db_session: Session) -> None:
    first_result = seed_prompts(db_session)
    second_result = seed_prompts(db_session)

    assert first_result == (6, 18)
    assert second_result == (0, 0)
    assert db_session.scalar(select(func.count()).select_from(Exercise)) == 6
    assert db_session.scalar(select(func.count()).select_from(Prompt)) == 18
