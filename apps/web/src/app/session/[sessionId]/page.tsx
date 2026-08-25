"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { RecordingWorkspace } from "@/components/recording/RecordingWorkspace";
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
        <RecordingWorkspace practiceSession={practiceSession} />
      ) : null}
    </main>
  );
}
