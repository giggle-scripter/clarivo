import type { Attempt, PracticeSession } from "@/types/api";

import { apiRequest } from "./client";


export function createPracticeSession(
  promptId: string,
): Promise<PracticeSession> {
  return apiRequest<PracticeSession>("/practice-sessions", {
    method: "POST",
    body: JSON.stringify({ prompt_id: promptId }),
  });
}

export function getPracticeSession(
  sessionId: string,
): Promise<PracticeSession> {
  return apiRequest<PracticeSession>(`/practice-sessions/${sessionId}`);
}

export function createAttempt(sessionId: string): Promise<Attempt> {
  return apiRequest<Attempt>(`/practice-sessions/${sessionId}/attempts`, {
    method: "POST",
  });
}
