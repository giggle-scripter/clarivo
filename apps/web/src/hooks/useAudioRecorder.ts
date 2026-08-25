"use client";

import { useCallback, useEffect, useRef, useState } from "react";


export type RecordingState =
  | "idle"
  | "requesting_permission"
  | "recording"
  | "stopped"
  | "error";


function getSupportedMimeType(): string | undefined {
  const candidates = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/mp4;codecs=mp4a.40.2",
    "audio/mp4",
  ];
  return candidates.find((type) => MediaRecorder.isTypeSupported(type));
}


export function useAudioRecorder(maxDurationMs: number) {
  const [state, setState] = useState<RecordingState>("idle");
  const [durationMs, setDurationMs] = useState(0);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const timerRef = useRef<number | null>(null);
  const startedAtRef = useRef(0);
  const chunksRef = useRef<Blob[]>([]);

  const clearTimer = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const closeStream = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
  }, []);

  const stopRecording = useCallback(() => {
    clearTimer();
    const recorder = recorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      recorder.stop();
    }
    closeStream();
  }, [clearTimer, closeStream]);

  const resetRecording = useCallback(() => {
    stopRecording();
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    recorderRef.current = null;
    chunksRef.current = [];
    setAudioBlob(null);
    setAudioUrl(null);
    setDurationMs(0);
    setError(null);
    setState("idle");
  }, [audioUrl, stopRecording]);

  const startRecording = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) {
      setError("Trình duyệt này chưa hỗ trợ tính năng ghi âm.");
      setState("error");
      return;
    }

    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioUrl(null);
    setAudioBlob(null);
    setDurationMs(0);
    setError(null);
    setState("requesting_permission");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      chunksRef.current = [];
      const mimeType = getSupportedMimeType();
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      recorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      };
      recorder.onerror = () => {
        setError("Quá trình ghi âm bị gián đoạn. Hãy thử lại.");
        setState("error");
        clearTimer();
        closeStream();
      };
      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, {
          type: recorder.mimeType || "audio/webm",
        });
        setDurationMs(Math.min(Date.now() - startedAtRef.current, maxDurationMs));
        setAudioBlob(blob);
        setAudioUrl(URL.createObjectURL(blob));
        setState("stopped");
      };

      startedAtRef.current = Date.now();
      recorder.start(250);
      setState("recording");
      timerRef.current = window.setInterval(() => {
        const elapsed = Date.now() - startedAtRef.current;
        setDurationMs(Math.min(elapsed, maxDurationMs));
        if (elapsed >= maxDurationMs) stopRecording();
      }, 100);
    } catch (reason) {
      closeStream();
      const permissionDenied =
        reason instanceof DOMException &&
        ["NotAllowedError", "PermissionDeniedError"].includes(reason.name);
      setError(
        permissionDenied
          ? "Clarivo chưa được cấp quyền dùng micrô. Hãy cho phép trong cài đặt trình duyệt."
          : "Không tìm thấy micrô khả dụng.",
      );
      setState("error");
    }
  }, [audioUrl, clearTimer, closeStream, maxDurationMs, stopRecording]);

  useEffect(() => {
    return () => {
      clearTimer();
      closeStream();
    };
  }, [clearTimer, closeStream]);

  return {
    state,
    durationMs,
    audioBlob,
    audioUrl,
    error,
    startRecording,
    stopRecording,
    resetRecording,
  };
}
