import type { Attempt } from "@/types/api";

import { API_URL, apiRequest } from "./client";


export function getAttempt(attemptId: string): Promise<Attempt> {
  return apiRequest<Attempt>(`/attempts/${attemptId}`);
}

export function uploadAttemptAudio(
  attemptId: string,
  audioBlob: Blob,
  durationMs: number,
): Promise<Attempt> {
  const formData = new FormData();
  const extension = audioBlob.type.includes("mp4") ? "m4a" : "webm";
  formData.append("duration_ms", Math.round(durationMs).toString());
  formData.append("audio", audioBlob, `attempt.${extension}`);
  return apiRequest<Attempt>(`/attempts/${attemptId}/audio`, {
    method: "POST",
    body: formData,
  });
}

export function getAttemptAudioUrl(attemptId: string): string {
  return `${API_URL}/attempts/${attemptId}/audio`;
}
