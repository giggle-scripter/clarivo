import type { Exercise, ExerciseDetail } from "@/types/api";

import { apiRequest } from "./client";


export function getExercises(): Promise<Exercise[]> {
  return apiRequest<Exercise[]>("/exercises");
}

export function getExercise(exerciseId: string): Promise<ExerciseDetail> {
  return apiRequest<ExerciseDetail>(`/exercises/${exerciseId}`);
}
