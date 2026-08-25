"use client";

import { useEffect, useState } from "react";

import { ExerciseCard } from "@/components/practice/ExerciseCard";
import { StatusMessage } from "@/components/ui/StatusMessage";
import { getExercises } from "@/lib/api/exercises";
import type { Exercise } from "@/types/api";


export default function PracticePage() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getExercises()
      .then(setExercises)
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : "Không thể tải bài luyện.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="content-page">
      <section className="page-intro">
        <p className="eyebrow">Practice library</p>
        <h1>Hôm nay bạn muốn nói rõ hơn trong tình huống nào?</h1>
        <p>
          Chọn một dạng bài. Mỗi lượt gồm 15 giây chuẩn bị, 60 giây trình bày
          và một lần thử lại có mục tiêu.
        </p>
      </section>

      {loading ? (
        <StatusMessage
          title="Đang tải bài luyện"
          detail="Clarivo đang lấy danh sách exercise từ API."
        />
      ) : null}

      {error ? (
        <StatusMessage
          title="Chưa kết nối được API"
          detail={`${error} Hãy kiểm tra FastAPI đang chạy ở port 8000.`}
          tone="error"
        />
      ) : null}

      {!loading && !error ? (
        <section className="exercise-grid" aria-label="Danh sách bài luyện">
          {exercises.map((exercise, index) => (
            <ExerciseCard exercise={exercise} index={index} key={exercise.id} />
          ))}
        </section>
      ) : null}
    </main>
  );
}
