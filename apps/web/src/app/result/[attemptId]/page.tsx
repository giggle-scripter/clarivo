"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { StatusMessage } from "@/components/ui/StatusMessage";
import { getAttempt, getAttemptAudioUrl } from "@/lib/api/attempts";
import type { Attempt } from "@/types/api";


export default function ResultPage() {
  const params = useParams<{ attemptId: string }>();
  const [attempt, setAttempt] = useState<Attempt | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAttempt(params.attemptId)
      .then(setAttempt)
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : "Không thể tải attempt.");
      });
  }, [params.attemptId]);

  return (
    <main className="content-page content-page--narrow">
      {!attempt && !error ? (
        <StatusMessage title="Đang tải bản ghi" detail="Clarivo đang mở attempt vừa tạo." />
      ) : null}

      {error ? (
        <StatusMessage title="Không thể tải attempt" detail={error} tone="error" />
      ) : null}

      {attempt ? (
        <section className="result-card">
          <div className="result-card__heading">
            <div>
              <p className="eyebrow">Attempt {attempt.attempt_number}</p>
              <h1>Bản ghi đã được lưu</h1>
            </div>
            <span className="complete-chip">Upload thành công</span>
          </div>
          <audio
            controls
            preload="metadata"
            src={getAttemptAudioUrl(attempt.id)}
          >
            Trình duyệt không hỗ trợ phát audio.
          </audio>
          <div className="result-meta">
            <div>
              <span>Thời lượng</span>
              <strong>{((attempt.audio_duration_ms ?? 0) / 1000).toFixed(1)}s</strong>
            </div>
            <div>
              <span>Định dạng</span>
              <strong>{attempt.audio_mime_type ?? "—"}</strong>
            </div>
            <div>
              <span>Trạng thái</span>
              <strong>{attempt.status}</strong>
            </div>
          </div>
          <div className="coming-next">
            <span>Tiếp theo trong roadmap</span>
            <p>Audio → ASR → transcript → delivery analysis.</p>
          </div>
          <div className="playback-actions">
            <Link
              className="button button--secondary"
              href={`/session/${attempt.practice_session_id}`}
            >
              Retry cùng prompt
            </Link>
            <Link className="button button--primary" href="/practice">
              Chọn bài khác →
            </Link>
          </div>
        </section>
      ) : null}
    </main>
  );
}
