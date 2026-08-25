import type { ExerciseType } from "@/types/api";


export const exerciseLabels: Record<ExerciseType, string> = {
  DAILY_60: "Một phút mỗi ngày",
  OPINION: "Quan điểm",
  INTERVIEW: "Phỏng vấn",
  TECHNICAL_EXPLANATION: "Giải thích kỹ thuật",
  STORYTELLING: "Kể chuyện",
  SUMMARY: "Tóm tắt",
};

export const exerciseEyebrows: Record<ExerciseType, string> = {
  DAILY_60: "Rèn thói quen mỗi ngày",
  OPINION: "Điểm · Lý do · Ví dụ",
  INTERVIEW: "Bối cảnh · Nhiệm vụ · Hành động · Kết quả",
  TECHNICAL_EXPLANATION: "Nội dung · Cách hoạt động · Ví dụ · Lý do",
  STORYTELLING: "Bối cảnh · Diễn biến · Kết quả",
  SUMMARY: "Ý chính · Luận điểm quan trọng",
};

const topicLabels: Record<string, string> = {
  challenges: "thử thách",
  education: "giáo dục",
  growth: "trưởng thành",
  habits: "thói quen",
  introduction: "giới thiệu",
  learning: "học tập",
  "machine-learning": "học máy",
  media: "nội dung",
  planning: "kế hoạch",
  projects: "dự án",
  reading: "đọc hiểu",
  software: "phần mềm",
  technology: "công nghệ",
  teamwork: "làm việc nhóm",
  work: "công việc",
  "work-study": "học tập và công việc",
};

const skillLabels: Record<string, string> = {
  coherence: "mạch lạc",
  conciseness: "súc tích",
  relevance: "đúng trọng tâm",
  specificity: "cụ thể",
  structure: "có cấu trúc",
};

export function getTopicLabel(topic: string): string {
  return topicLabels[topic] ?? topic.replaceAll("-", " ");
}

export function getSkillLabel(skill: string): string {
  return skillLabels[skill] ?? skill.replaceAll("-", " ");
}
