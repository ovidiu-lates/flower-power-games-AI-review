import { FormEvent, useState } from "react";
import { Star, X } from "lucide-react";
import { createReview } from "../services/gameService";

interface WriteReviewModalProps {
  gameId: string;
  gameName: string;
  onClose: () => void;
  onCreated: () => void;
}

export default function WriteReviewModal({ gameId, gameName, onClose, onCreated }: WriteReviewModalProps) {
  const [rating, setRating] = useState(8);
  const [content, setContent] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await createReview(gameId, rating, content);
      onCreated();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not publish your review.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="review-title">
        <button className="icon-button modal__close" onClick={onClose} aria-label="Close"><X size={19} /></button>
        <span className="eyebrow">Share your experience</span>
        <h2 id="review-title">Review {gameName}</h2>
        <form onSubmit={submit}>
          <label htmlFor="rating">Rating <span>{rating}/10</span></label>
          <div className="rating-control">
            <Star size={20} fill="currentColor" />
            <input id="rating" type="range" min="1" max="10" value={rating} onChange={(event) => setRating(Number(event.target.value))} />
          </div>
          <label htmlFor="review">Your review</label>
          <textarea id="review" rows={6} minLength={1} required value={content} onChange={(event) => setContent(event.target.value)} placeholder="What worked, what didn't, and who would enjoy it?" />
          {error && <p className="form-error" role="alert">{error}</p>}
          <div className="modal__actions">
            <button type="button" className="button button--secondary" onClick={onClose}>Cancel</button>
            <button className="button button--primary" disabled={submitting}>{submitting ? "Publishing..." : "Publish review"}</button>
          </div>
        </form>
      </section>
    </div>
  );
}