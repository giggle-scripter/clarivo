export type ExerciseType =
  | "DAILY_60"
  | "OPINION"
  | "INTERVIEW"
  | "TECHNICAL_EXPLANATION"
  | "STORYTELLING"
  | "SUMMARY";

export interface Prompt {
  id: string;
  exercise_id: string;
  text: string;
  topic: string;
  target_skills: string[];
  is_active: boolean;
  created_at: string;
}

export interface Exercise {
  id: string;
  slug: string;
  name: string;
  description: string;
  exercise_type: ExerciseType;
  difficulty: number;
  prep_seconds: number;
  speak_seconds: number;
  created_at: string;
}

export interface ExerciseDetail extends Exercise {
  prompts: Prompt[];
}

export type AttemptStatus = "CREATED" | "UPLOADED";

export interface Attempt {
  id: string;
  practice_session_id: string;
  attempt_number: number;
  status: AttemptStatus;
  audio_url: string | null;
  audio_duration_ms: number | null;
  audio_mime_type: string | null;
  created_at: string;
}

export interface PracticeSession {
  id: string;
  user_id: string | null;
  exercise_id: string;
  prompt_id: string;
  status: "ACTIVE" | "COMPLETED";
  started_at: string;
  completed_at: string | null;
  prompt: Prompt;
  attempts: Attempt[];
}
