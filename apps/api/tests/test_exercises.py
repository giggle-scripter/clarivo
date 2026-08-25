from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import Exercise, ExerciseType, Prompt


def create_exercise_with_prompts(db: Session) -> Exercise:
    exercise = Exercise(
        slug="technical-explanation",
        name="Technical Explanation",
        description="Explain a technical idea clearly.",
        exercise_type=ExerciseType.TECHNICAL_EXPLANATION,
        difficulty=2,
        prep_seconds=15,
        speak_seconds=60,
        prompts=[
            Prompt(
                text="Hãy giải thích project gần nhất của bạn.",
                topic="projects",
                target_skills=["structure", "conciseness"],
            ),
            Prompt(
                text="Đây là prompt đã tắt.",
                topic="inactive",
                target_skills=[],
                is_active=False,
            ),
        ],
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def test_list_exercises(client: TestClient, db_session: Session) -> None:
    exercise = create_exercise_with_prompts(db_session)

    response = client.get("/exercises")

    assert response.status_code == 200
    assert response.json()[0]["id"] == str(exercise.id)
    assert response.json()[0]["exercise_type"] == "TECHNICAL_EXPLANATION"


def test_get_exercise_returns_only_active_prompts(
    client: TestClient,
    db_session: Session,
) -> None:
    exercise = create_exercise_with_prompts(db_session)

    response = client.get(f"/exercises/{exercise.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["slug"] == "technical-explanation"
    assert len(body["prompts"]) == 1
    assert body["prompts"][0]["is_active"] is True


def test_get_missing_exercise_returns_404(client: TestClient) -> None:
    response = client.get("/exercises/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Exercise not found"}
