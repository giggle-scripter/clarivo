import type { Attempt } from "@/types/api";

import { apiRequest } from "./client";


export function getAttempt(attemptId: string): Promise<Attempt> {
  return apiRequest<Attempt>(`/attempts/${attemptId}`);
}
