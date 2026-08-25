"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { StatusMessage } from "@/components/ui/StatusMessage";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import { uploadAttemptAudio } from "@/lib/api/attempts";
import { createAttempt } from "@/lib/api/sessions";
import type { PracticeSession } from "@/types/api";


interface RecordingWorkspaceProps {
  practiceSession: PracticeSession;
}


type PreparationState = "ready" | "preparing" | "complete";


function formatDuration(durationMs: number): string {
  const totalSeconds = Math.floor(durationMs / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}


export function RecordingWorkspace({ practiceSession }: RecordingWorkspaceProps) {
  const router = useRouter();
  const prepSeconds = 15;
  const maxDurationMs = 60_000;
  const [preparation, setPreparation] = useState<PreparationState>("ready");
  const [prepRemaining, setPrepRemaining] = useState(prepSeconds);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const recorder = useAudioRecorder(maxDurationMs);

  useEffect(() => {
    if (preparation !== "preparing") return;
    if (prepRemaining <= 0) {
      setPreparation("complete");
      return;
    }
    const timer = window.setTimeout(
      () => setPrepRemaining((value) => value - 1),
      1000,
    );
    return () => window.clearTimeout(timer);
  }, [prepRemaining, preparation]);

  function beginPreparation() {
    setPrepRemaining(prepSeconds);
    setPreparation("preparing");
  }

  async function submitAttempt() {
    if (!recorder.audioBlob || recorder.durationMs < 1000) return;
    setUploading(true);
    setUploadError(null);
    try {
      const attempt = await createAttempt(practiceSession.id);
      const uploadedAttempt = await uploadAttemptAudio(
        attempt.id,
        recorder.audioBlob,
        recorder.durationMs,
      );
      router.push(`/result/${uploadedAttempt.id}`);
    } catch (reason) {
      setUploadError(
        reason instanceof Error ? reason.message : "Không thể lưu bản ghi.",
      );
      setUploading(false);
    }
  }

  return (
    <section className="session-stage recording-workspace">
      <div className="session-topline">
        <p className="eyebrow">Câu hỏi của bạn</p>
        <span>Lần nói {practiceSession.attempts.length + 1}</span>
      </div>
      <h1>{practiceSession.prompt.text}</h1>
      <div className="session-rule" />

      {preparation === "ready" ? (
        <div className="recorder-panel">
          <span className="record-icon" aria-hidden="true" />
          <h2>Sẵn sàng gom ý?</h2>
          <p>Bạn có 15 giây để chọn ý chính, lý do và một ví dụ cụ thể.</p>
          <button
            className="button button--primary"
            onClick={beginPreparation}
            type="button"
          >
            Bắt đầu chuẩn bị →
          </button>
        </div>
      ) : null}

      {preparation === "preparing" ? (
        <div className="recorder-panel preparation-panel">
          <div className="countdown-ring" aria-live="polite">
            <strong>{prepRemaining}</strong>
            <span>giây</span>
          </div>
          <h2>Chốt câu đầu tiên</h2>
          <p>Đừng viết cả bài. Chỉ cần biết bạn sẽ trả lời trực tiếp bằng câu nào.</p>
          <button
            className="text-button"
            onClick={() => setPreparation("complete")}
            type="button"
          >
            Tôi đã sẵn sàng, bỏ qua thời gian còn lại
          </button>
        </div>
      ) : null}

      {preparation === "complete" && recorder.state === "idle" ? (
        <div className="recorder-panel">
          <div className="mic-orbit" aria-hidden="true">
            <span />
          </div>
          <h2>Bắt đầu khi bạn sẵn sàng</h2>
          <p>Trình duyệt sẽ xin quyền dùng micrô trong lần ghi âm đầu tiên.</p>
          <button
            className="button button--record"
            onClick={recorder.startRecording}
            type="button"
          >
            <span aria-hidden="true" /> Ghi âm
          </button>
        </div>
      ) : null}

      {recorder.state === "requesting_permission" ? (
        <StatusMessage
          title="Đang chờ quyền dùng micrô"
          detail="Chọn Cho phép trong hộp thoại của trình duyệt để tiếp tục."
        />
      ) : null}

      {recorder.state === "recording" ? (
        <div className="recorder-panel recorder-panel--active">
          <div className="recording-badge">
            <i /> Đang ghi âm
          </div>
          <strong className="recording-time">
            {formatDuration(recorder.durationMs)}
          </strong>
          <div className="live-wave" aria-hidden="true">
            {Array.from({ length: 32 }).map((_, index) => (
              <i key={index} />
            ))}
          </div>
          <p>Tối đa {formatDuration(maxDurationMs)} · nói tự nhiên, không cần hoàn hảo.</p>
          <button
            className="button button--stop"
            onClick={recorder.stopRecording}
            type="button"
          >
            <span aria-hidden="true" /> Dừng ghi âm
          </button>
        </div>
      ) : null}

      {recorder.state === "stopped" && recorder.audioUrl ? (
        <div className="recorder-panel playback-panel">
          <div className="playback-heading">
            <div>
              <p className="eyebrow">Bản ghi của bạn</p>
              <h2>{formatDuration(recorder.durationMs)}</h2>
            </div>
            <span className="complete-chip">Đã ghi xong</span>
          </div>
          <audio controls preload="metadata" src={recorder.audioUrl}>
            Trình duyệt không hỗ trợ phát bản ghi âm.
          </audio>
          {recorder.durationMs < 1000 ? (
            <p className="validation-note">Bản ghi quá ngắn. Hãy thử lại ít nhất 1 giây.</p>
          ) : null}
          {uploadError ? (
            <StatusMessage title="Chưa lưu được bản ghi" detail={uploadError} tone="error" />
          ) : null}
          <div className="playback-actions">
            <button
              className="button button--secondary"
              disabled={uploading}
              onClick={recorder.resetRecording}
              type="button"
            >
              Ghi lại
            </button>
            <button
              className="button button--primary"
              disabled={uploading || recorder.durationMs < 1000}
              onClick={submitAttempt}
              type="button"
            >
              {uploading ? "Đang lưu bản ghi..." : "Lưu bản ghi →"}
            </button>
          </div>
        </div>
      ) : null}

      {recorder.state === "error" ? (
        <div>
          <StatusMessage
            title="Chưa thể ghi âm"
            detail={recorder.error ?? "Hãy kiểm tra micrô và thử lại."}
            tone="error"
          />
          <button
            className="button button--secondary"
            onClick={recorder.resetRecording}
            type="button"
          >
            Thử lại
          </button>
        </div>
      ) : null}
    </section>
  );
}
