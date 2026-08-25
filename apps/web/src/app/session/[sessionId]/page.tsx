"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { StatusMessage } from "@/components/ui/StatusMessage";
import { getPracticeSession } from "@/lib/api/sessions";
import type { PracticeSession } from "@/types/api";


export default function SessionPage() {
  const params = useParams<{ sessionId: string }>();
  const [practiceSession, setPracticeSession] = useState<PracticeSession | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPracticeSession(params.sessionId)
      .then(setPracticeSession)
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : "Không thể tải session.");
      });
  }, [params.sessionId]);

  return (
    <main className="content-page content-page--narrow">
      <Link className="back-link" href="/practice">
        ← Chọn câu hỏi khác
      </Link>

      {!practiceSession && !error ? (
        <StatusMessage title="Đang mở session" detail="Clarivo đang lấy prompt của bạn." />
      ) : null}

      {error ? (
        <StatusMessage title="Không thể mở session" detail={error} tone="error" />
      ) : null}

      {practiceSession ? (
        <section className="session-stage">
          <p className="eyebrow">Prompt của bạn</p>
          <h1>{practiceSession.prompt.text}</h1>
          <div className="session-rule" />
          <div className="session-placeholder">
            <span className="record-icon" aria-hidden="true" />
            <h2>Session đã sẵn sàng</h2>
            <p>
              Luồng tạo session đã hoàn tất. Recorder sẽ được kết nối trong
              checkpoint tiếp theo.
            </p>
          </div>
        </section>
      ) : null}
    </main>
  );
}
