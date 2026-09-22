import type { Difficulty, Sentiment } from "../types/game";

const sentimentConfig: Record<Sentiment, { bg: string; text: string; label: string }> = {
  positive: { bg: "#DCFCE7", text: "#15803D", label: "Positive" },
  mixed: { bg: "#FEF3C7", text: "#B45309", label: "Mixed" },
  neutral: { bg: "#F3F4F6", text: "#4B5563", label: "Neutral" },
  negative: { bg: "#FEE2E2", text: "#B91C1C", label: "Negative" },
};

const difficultyConfig: Record<Difficulty, { bg: string; text: string; label: string }> = {
  easy: { bg: "#DBEAFE", text: "#1D4ED8", label: "Easy" },
  medium: { bg: "#FEF3C7", text: "#B45309", label: "Medium" },
  hard: { bg: "#FCE7F3", text: "#9D174D", label: "Hard" },
};

export function SentimentBadge({ sentiment }: { sentiment: Sentiment }) {
  const config = sentimentConfig[sentiment];

  return (
    <span className="badge" style={{ backgroundColor: config.bg, color: config.text }}>
      <span className="badge-dot" style={{ backgroundColor: config.text }} />
      {config.label}
    </span>
  );
}

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty | null }) {
  if (!difficulty) {
    return <span className="badge badge-muted">No insight</span>;
  }

  const config = difficultyConfig[difficulty];

  return (
    <span className="badge" style={{ backgroundColor: config.bg, color: config.text }}>
      {config.label}
    </span>
  );
}

export function Tag({ label }: { label: string }) {
  return <span className="tag">{label}</span>;
}