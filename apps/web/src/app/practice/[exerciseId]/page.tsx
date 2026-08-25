"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { PromptCard } from "@/components/practice/PromptCard";
import { StatusMessage } from "@/components/ui/StatusMessage";
import { getExercise } from "@/lib/api/exercises";
import { createPracticeSession } from "@/lib/api/sessions";
import { exerciseLabels } from "@/lib/exercise-labels";
import type { ExerciseDetail } from "@/types/api";


export default function ExerciseDetailPage() {
  const params = useParams<{ exerciseId: string }>();
  const router = useRouter();
  const [exercise, setExercise] = useState<ExerciseDetail | null>(null);
  const [selectedPromptId, setSelectedPromptId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    getExercise(params.exerciseId)
      .then((result) => {
        setExercise(result);
        setSelectedPromptId(result.prompts[0]?.id ?? null);
      })
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : "Không thể tải câu hỏi.");
      });
  }, [params.exerciseId]);

  async function startSession() {
    if (!selectedPromptId) return;
    setStarting(true);
    setError(null);
    try {
      const practiceSession = await createPracticeSession(selectedPromptId);
      router.push(`/session/${practiceSession.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể bắt đầu buổi luyện.");
      setStarting(false);
    }
  }

  return (
    <main className="content-page content-page--narrow">
      <Link className="back-link" href="/practice">
        ← Quay lại thư viện
      </Link>

      {!exercise && !error ? (
        <StatusMessage title="Đang tải câu hỏi" detail="Chỉ còn một chút nữa." />
      ) : null}

      {exercise ? (
        <>
          <section className="exercise-heading">
            <div>
              <p className="eyebrow">{exerciseLabels[exercise.exercise_type]}</p>
              <h1>Chọn một câu hỏi để bắt đầu</h1>
            </div>
            <div className="timing-card">
              <span>{exercise.prep_seconds}s</span>
              <small>chuẩn bị</small>
              <i />
              <span>{exercise.speak_seconds}s</span>
              <small>trình bày</small>
            </div>
          </section>

          <section className="prompt-list" aria-label="Danh sách câu hỏi">
            {exercise.prompts.map((prompt) => (
              <PromptCard
                disabled={starting}
                key={prompt.id}
                onSelect={setSelectedPromptId}
                prompt={prompt}
                selected={prompt.id === selectedPromptId}
              />
            ))}
          </section>

          {error ? (
            <StatusMessage title="Không thể bắt đầu" detail={error} tone="error" />
          ) : null}

          <div className="sticky-action">
            <div>
              <span className="status-dot" />
              <p>Trình duyệt sẽ xin quyền dùng micrô ở bước tiếp theo.</p>
            </div>
            <button
              className="button button--primary"
              disabled={!selectedPromptId || starting}
              onClick={startSession}
              type="button"
            >
              {starting ? "Đang mở buổi luyện..." : "Bắt đầu chuẩn bị →"}
            </button>
          </div>
        </>
      ) : null}

      {error && !exercise ? (
        <StatusMessage title="Không tải được bài luyện" detail={error} tone="error" />
      ) : null}
    </main>
  );
}
