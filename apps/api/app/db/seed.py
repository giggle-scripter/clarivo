from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Exercise, ExerciseType, Prompt
from app.db.session import SessionLocal


EXERCISE_SEEDS: tuple[dict[str, Any], ...] = (
    {
        "slug": "daily-60",
        "name": "Daily 60",
        "description": "Luyện trình bày một ý rõ ràng trong 60 giây.",
        "exercise_type": ExerciseType.DAILY_60,
        "difficulty": 1,
        "prompts": (
            ("Hãy nói về một thói quen bạn muốn thay đổi.", "habits"),
            ("Hãy chia sẻ một điều hữu ích bạn mới học được.", "learning"),
            ("Điều gì là ưu tiên quan trọng nhất của bạn trong tuần này?", "planning"),
        ),
        "target_skills": ["structure", "conciseness"],
    },
    {
        "slug": "opinion",
        "name": "Opinion",
        "description": "Nêu quan điểm, lý do và ví dụ thuyết phục.",
        "exercise_type": ExerciseType.OPINION,
        "difficulty": 2,
        "prompts": (
            ("Làm việc nhóm hay làm việc cá nhân hiệu quả hơn?", "work"),
            ("Học trực tuyến có thể thay thế hoàn toàn lớp học trực tiếp không?", "education"),
            ("Sinh viên có nên sử dụng AI trong học tập không?", "technology"),
        ),
        "target_skills": ["relevance", "structure", "specificity"],
    },
    {
        "slug": "interview",
        "name": "Interview",
        "description": "Luyện trả lời phỏng vấn ngắn gọn và có bằng chứng.",
        "exercise_type": ExerciseType.INTERVIEW,
        "difficulty": 2,
        "prompts": (
            ("Hãy giới thiệu bản thân trong 60 giây.", "introduction"),
            ("Hãy mô tả một lần bạn gặp khó khăn trong một project.", "challenges"),
            ("Hãy kể về một lần bạn bất đồng ý kiến với đồng đội.", "teamwork"),
        ),
        "target_skills": ["structure", "relevance", "specificity"],
    },
    {
        "slug": "technical-explanation",
        "name": "Technical Explanation",
        "description": "Giải thích khái niệm kỹ thuật cho đúng đối tượng nghe.",
        "exercise_type": ExerciseType.TECHNICAL_EXPLANATION,
        "difficulty": 3,
        "prompts": (
            ("Hãy giải thích project gần đây nhất của bạn.", "projects"),
            ("Giải thích overfitting cho người chưa học machine learning.", "machine-learning"),
            ("Giải thích API là gì cho một người không làm kỹ thuật.", "software"),
        ),
        "target_skills": ["structure", "coherence", "conciseness"],
    },
    {
        "slug": "storytelling",
        "name": "Storytelling",
        "description": "Kể một câu chuyện có diễn biến và kết quả rõ ràng.",
        "exercise_type": ExerciseType.STORYTELLING,
        "difficulty": 2,
        "prompts": (
            ("Hãy kể về một sai lầm đã giúp bạn học được điều quan trọng.", "learning"),
            ("Hãy kể về một lần bạn thay đổi quan điểm của mình.", "growth"),
            ("Hãy kể về một lần hợp tác nhóm thành công.", "teamwork"),
        ),
        "target_skills": ["structure", "coherence", "specificity"],
    },
    {
        "slug": "summary",
        "name": "Summary",
        "description": "Tóm tắt nội dung và giữ lại các ý quan trọng nhất.",
        "exercise_type": ExerciseType.SUMMARY,
        "difficulty": 2,
        "prompts": (
            ("Hãy tóm tắt một bài báo bạn đọc gần đây.", "reading"),
            ("Hãy tóm tắt nội dung chính của một video bạn vừa xem.", "media"),
            ("Hãy tóm tắt một buổi học hoặc cuộc họp gần đây.", "work-study"),
        ),
        "target_skills": ["relevance", "conciseness", "coherence"],
    },
)


def seed_prompts(db: Session) -> tuple[int, int]:
    created_exercises = 0
    created_prompts = 0

    for seed in EXERCISE_SEEDS:
        exercise = db.scalar(
            select(Exercise).where(Exercise.slug == seed["slug"])
        )
        if exercise is None:
            exercise = Exercise(
                slug=seed["slug"],
                name=seed["name"],
                description=seed["description"],
                exercise_type=seed["exercise_type"],
                difficulty=seed["difficulty"],
                prep_seconds=15,
                speak_seconds=60,
            )
            db.add(exercise)
            db.flush()
            created_exercises += 1

        existing_texts = set(
            db.scalars(
                select(Prompt.text).where(Prompt.exercise_id == exercise.id)
            ).all()
        )
        for prompt_text, topic in seed["prompts"]:
            if prompt_text in existing_texts:
                continue
            db.add(
                Prompt(
                    exercise_id=exercise.id,
                    text=prompt_text,
                    topic=topic,
                    target_skills=seed["target_skills"],
                )
            )
            created_prompts += 1

    db.commit()
    return created_exercises, created_prompts


def main() -> None:
    with SessionLocal() as db:
        exercise_count, prompt_count = seed_prompts(db)
    print(f"Created {exercise_count} exercises and {prompt_count} prompts.")


if __name__ == "__main__":
    main()
