from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import Exercise, ExerciseType, Prompt


def create_prompt(db: Session, *, is_active: bool = True) -> Prompt:
    exercise = Exercise(
        slug="daily-session-test",
        name="Daily Session Test",
        description="Session API fixture.",
        exercise_type=ExerciseType.DAILY_60,
        difficulty=1,
        prep_seconds=15,
        speak_seconds=60,
    )
    prompt = Prompt(
        exercise=exercise,
        text="Hãy trình bày mục tiêu quan trọng nhất hôm nay.",
        topic="planning",
        target_skills=["structure"],
        is_active=is_active,
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


def test_create_and_get_practice_session(
    client: TestClient,
    db_session: Session,
) -> None:
    prompt = create_prompt(db_session)

    create_response = client.post(
        "/practice-sessions",
        json={"prompt_id": str(prompt.id)},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["prompt_id"] == str(prompt.id)
    assert created["exercise_id"] == str(prompt.exercise_id)
    assert created["status"] == "ACTIVE"
    assert created["attempts"] == []

    get_response = client.get(f"/practice-sessions/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["prompt"]["text"] == prompt.text


def test_attempt_numbers_increment_within_session(
    client: TestClient,
    db_session: Session,
) -> None:
    prompt = create_prompt(db_session)
    practice_session = client.post(
        "/practice-sessions",
        json={"prompt_id": str(prompt.id)},
    ).json()

    first = client.post(
        f"/practice-sessions/{practice_session['id']}/attempts"
    )
    second = client.post(
        f"/practice-sessions/{practice_session['id']}/attempts"
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["attempt_number"] == 1
    assert second.json()["attempt_number"] == 2
    assert first.json()["status"] == "CREATED"

    get_attempt = client.get(f"/attempts/{second.json()['id']}")
    assert get_attempt.status_code == 200
    assert get_attempt.json()["practice_session_id"] == practice_session["id"]

    get_session = client.get(f"/practice-sessions/{practice_session['id']}")
    assert [item["attempt_number"] for item in get_session.json()["attempts"]] == [
        1,
        2,
    ]


def test_inactive_prompt_cannot_start_session(
    client: TestClient,
    db_session: Session,
) -> None:
    prompt = create_prompt(db_session, is_active=False)

    response = client.post(
        "/practice-sessions",
        json={"prompt_id": str(prompt.id)},
    )

    assert response.status_code == 404
