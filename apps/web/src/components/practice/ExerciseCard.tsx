import Link from "next/link";

import { exerciseEyebrows, exerciseLabels } from "@/lib/exercise-labels";
import type { Exercise } from "@/types/api";


interface ExerciseCardProps {
  exercise: Exercise;
  index: number;
}


export function ExerciseCard({ exercise, index }: ExerciseCardProps) {
  return (
    <Link className="exercise-card" href={`/practice/${exercise.id}`}>
      <div className="exercise-card__topline">
        <span className="exercise-index">{String(index + 1).padStart(2, "0")}</span>
        <span className="difficulty">Độ khó {exercise.difficulty}/3</span>
      </div>
      <div>
        <p className="eyebrow">{exerciseEyebrows[exercise.exercise_type]}</p>
        <h2>{exerciseLabels[exercise.exercise_type]}</h2>
        <p className="muted">{exercise.description}</p>
      </div>
      <div className="exercise-card__meta">
        <span>{exercise.prep_seconds}s chuẩn bị</span>
        <span>{exercise.speak_seconds}s trình bày</span>
        <span className="arrow" aria-hidden="true">
          →
        </span>
      </div>
    </Link>
  );
}
