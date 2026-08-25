import type { Prompt } from "@/types/api";


interface PromptCardProps {
  prompt: Prompt;
  selected: boolean;
  disabled: boolean;
  onSelect: (promptId: string) => void;
}


export function PromptCard({
  prompt,
  selected,
  disabled,
  onSelect,
}: PromptCardProps) {
  return (
    <button
      className={`prompt-card${selected ? " prompt-card--selected" : ""}`}
      disabled={disabled}
      onClick={() => onSelect(prompt.id)}
      type="button"
    >
      <span className="prompt-radio" aria-hidden="true" />
      <span className="prompt-card__content">
        <span className="prompt-topic">{prompt.topic.replaceAll("-", " ")}</span>
        <strong>{prompt.text}</strong>
        <span className="skill-list">
          {prompt.target_skills.map((skill) => (
            <span key={skill}>{skill}</span>
          ))}
        </span>
      </span>
    </button>
  );
}
