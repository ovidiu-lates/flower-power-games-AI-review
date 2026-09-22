import { Star } from "lucide-react";
import type { Review } from "../types/game";

export default function ReviewCard({ review }: { review: Review }) {
  return (
    <article className="review-card">
      <div className="review-card__meta">
        <span className="review-card__avatar">{review.user_id.slice(0, 2).toUpperCase()}</span>
        <div>
          <strong>Player review</strong>
          <time dateTime={review.created_at}>{new Date(review.created_at).toLocaleDateString()}</time>
        </div>
        <span className="rating"><Star size={15} fill="currentColor" /> {review.rating}/10</span>
      </div>
      <div className="review-card__body"><p>“{review.content}”</p></div>
    </article>
  );
}