import { AlertCircle, BrainCircuit, Sparkles, ThumbsDown, ThumbsUp } from "lucide-react";
import { useState } from "react";
import { explainGameInsight } from "../services/gameService";
import type { GameInsight } from "../types/api";

export default function InsightsPanel({ insight }: { insight: GameInsight }) {
  const [reviewCount, setReviewCount] = useState(Math.min(10, Math.max(1, insight.total_reviews)));
  const [explanation, setExplanation] = useState("");
  const [explanationError, setExplanationError] = useState("");
  const [explaining, setExplaining] = useState(false);
  const sentimentStops = `${insight.positive_percentage}% ${insight.positive_percentage + insight.neutral_percentage}%`;

  async function explain() {
    setExplaining(true);
    setExplanationError("");
    try {
      const response = await explainGameInsight(insight.game_id, reviewCount);
      setExplanation(response.explanation);
    } catch (caught) {
      setExplanationError(caught instanceof Error ? caught.message : "Could not explain these insights.");
    } finally {
      setExplaining(false);
    }
  }

  return (
    <section className="panel insights-panel">
      <div className="section-heading">
        <div><h2>Review Insights</h2><span className="insight-source"><Sparkles size={13} /> AI-generated from player reviews</span></div>
        <span className="data-note">Updated {new Date(insight.generated_at).toLocaleDateString()}</span>
      </div>

      <div className="insight-overview">
        <div className="score-block"><strong>{insight.average_rating.toFixed(1)}</strong><span>average rating</span></div>
        <div className="sentiment-visual">
          <div className="donut" style={{ background: `conic-gradient(#2f855a 0 ${insight.positive_percentage}%, #d9a441 ${insight.positive_percentage}% ${sentimentStops}, #b94b3d ${insight.positive_percentage + insight.neutral_percentage}% 100%)` }}>
            <span>{Math.round(insight.positive_percentage)}%<small>positive</small></span>
          </div>
          <div className="legend"><span className="positive">Positive {Math.round(insight.positive_percentage)}%</span><span className="neutral">Neutral {Math.round(insight.neutral_percentage)}%</span><span className="negative">Negative {Math.round(insight.negative_percentage)}%</span></div>
        </div>
        <div className="difficulty-bars">
          {[{ label: "Easy", value: insight.easy_percentage }, { label: "Medium", value: insight.medium_percentage }, { label: "Hard", value: insight.hard_percentage }].map(({ label, value }) => (
            <div key={label}><span>{label}<strong>{Math.round(value)}%</strong></span><div className="bar"><i style={{ width: `${value}%` }} /></div></div>
          ))}
        </div>
      </div>

      <div className="insight-lists">
        <div><h3><ThumbsUp size={17} /> Most liked</h3>{insight.liked_aspects.slice(0, 4).map((item) => <div className="ranked-item" key={item.aspect}><span>{item.aspect}</span><small>{item.occurrence_count} mentions</small></div>)}</div>
        <div><h3><ThumbsDown size={17} /> Common complaints</h3>{insight.complaints.slice(0, 4).map((item) => <div className="ranked-item" key={item.complaint}><span>{item.complaint}</span><small>{item.occurrence_count} mentions</small></div>)}</div>
      </div>

      <div className="explain-controls">
        <label htmlFor="explanation-review-count">Reviews to include</label>
        <input
          id="explanation-review-count"
          type="number"
          min="1"
          max="20"
          value={reviewCount}
          onChange={(event) => setReviewCount(Math.min(20, Math.max(1, Number(event.target.value) || 1)))}
        />
        <button className="explain-button" onClick={explain} disabled={explaining}>
          <BrainCircuit size={18} /> {explaining ? "Explaining..." : "Explain these insights"}
        </button>
      </div>
      {explanationError && <p className="explanation-error" role="alert"><AlertCircle size={16} /> {explanationError}</p>}
      {explanation && <div className="explanation"><strong>AI explanation</strong><p>{explanation}</p><small>Generated from the latest {reviewCount} reviews and aggregated game insights.</small></div>}
    </section>
  );
}