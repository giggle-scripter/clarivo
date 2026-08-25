import type { ExerciseType } from "@/types/api";


export const exerciseLabels: Record<ExerciseType, string> = {
  DAILY_60: "Daily 60",
  OPINION: "Quan điểm",
  INTERVIEW: "Phỏng vấn",
  TECHNICAL_EXPLANATION: "Giải thích kỹ thuật",
  STORYTELLING: "Kể chuyện",
  SUMMARY: "Tóm tắt",
};

export const exerciseEyebrows: Record<ExerciseType, string> = {
  DAILY_60: "Rèn thói quen mỗi ngày",
  OPINION: "Điểm · Lý do · Ví dụ",
  INTERVIEW: "Situation · Task · Action · Result",
  TECHNICAL_EXPLANATION: "What · How · Example · Why",
  STORYTELLING: "Bối cảnh · Diễn biến · Kết quả",
  SUMMARY: "Ý chính · Luận điểm quan trọng",
};
