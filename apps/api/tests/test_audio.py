from io import BytesIO

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.deps import get_storage_service
from app.db.models import Exercise, ExerciseType, Prompt
from app.main import app
from app.services.storage_service import StoredAudio


class FakeStorageService:
    def __init__(self) -> None:
        self.objects: dict[str, tuple[bytes, str]] = {}
        self.bucket = "test-audio"

    def put_audio(self, *, object_key: str, file, content_type: str) -> str:
        file.seek(0)
        self.objects[object_key] = (file.read(), content_type)
        return f"s3://{self.bucket}/{object_key}"

    def get_audio(self, object_uri: str) -> StoredAudio:
        object_key = object_uri.removeprefix(f"s3://{self.bucket}/")
        content, content_type = self.objects[object_key]
        return StoredAudio(
            body=BytesIO(content),
            content_length=len(content),
            content_type=content_type,
        )


def create_attempt(client: TestClient, db: Session) -> dict:
    exercise = Exercise(
        slug="audio-test",
        name="Audio Test",
        description="Audio upload fixture.",
        exercise_type=ExerciseType.DAILY_60,
        difficulty=1,
        prep_seconds=15,
        speak_seconds=60,
    )
    prompt = Prompt(
        exercise=exercise,
        text="Hãy nói một câu ngắn.",
        topic="testing",
        target_skills=["fluency"],
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    practice_session = client.post(
        "/practice-sessions",
        json={"prompt_id": str(prompt.id)},
    ).json()
    return client.post(
        f"/practice-sessions/{practice_session['id']}/attempts"
    ).json()


def test_upload_and_stream_audio(client: TestClient, db_session: Session) -> None:
    storage = FakeStorageService()
    app.dependency_overrides[get_storage_service] = lambda: storage
    attempt = create_attempt(client, db_session)

    upload_response = client.post(
        f"/attempts/{attempt['id']}/audio",
        data={"duration_ms": "1250"},
        files={"audio": ("attempt.webm", b"fake-webm-audio", "audio/webm")},
    )

    assert upload_response.status_code == 200
    uploaded = upload_response.json()
    assert uploaded["status"] == "UPLOADED"
    assert uploaded["audio_duration_ms"] == 1250
    assert uploaded["audio_url"].startswith("s3://test-audio/")

    stream_response = client.get(f"/attempts/{attempt['id']}/audio")
    assert stream_response.status_code == 200
    assert stream_response.headers["content-type"] == "audio/webm"
    assert stream_response.content == b"fake-webm-audio"


def test_rejects_unsupported_audio_format(
    client: TestClient,
    db_session: Session,
) -> None:
    storage = FakeStorageService()
    app.dependency_overrides[get_storage_service] = lambda: storage
    attempt = create_attempt(client, db_session)

    response = client.post(
        f"/attempts/{attempt['id']}/audio",
        data={"duration_ms": "1250"},
        files={"audio": ("attempt.txt", b"not-audio", "text/plain")},
    )

    assert response.status_code == 415
    assert storage.objects == {}
