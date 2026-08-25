interface StatusMessageProps {
  title: string;
  detail: string;
  tone?: "neutral" | "error";
}


export function StatusMessage({
  title,
  detail,
  tone = "neutral",
}: StatusMessageProps) {
  return (
    <div className={`status-message status-message--${tone}`} role="status">
      <span className="status-dot" aria-hidden="true" />
      <div>
        <strong>{title}</strong>
        <p>{detail}</p>
      </div>
    </div>
  );
}
