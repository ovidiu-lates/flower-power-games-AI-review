import { Star, UserRound } from "lucide-react";
import { Link } from "react-router-dom";
import GameArtwork from "./GameArtwork";
import type { Review } from "../types/game";

type ReviewCardProps = {
  review: Review;
  gameName?: string;
  gameImageUrl?: string;
};

export default function ReviewCard({ review, gameName, gameImageUrl }: ReviewCardProps) {
  return (
    <article className="review-card">
      <div className="review-card__meta">
        {gameImageUrl ? (
          <span className="review-card__avatar review-card__game-artwork">
            <GameArtwork src={gameImageUrl} name={gameName ?? "Game"} />
          </span>
        ) : (
          <span className="review-card__avatar" aria-hidden="true"><UserRound size={17} /></span>
        )}
        <div>
          <strong>{gameName ? <Link to={`/games/${review.game_id}`}>{gameName}</Link> : "Player review"}</strong>
          <time dateTime={review.created_at}>{new Date(review.created_at).toLocaleDateString()}</time>
        </div>
        <span className="rating"><Star size={15} fill="currentColor" /> {review.rating}/10</span>
      </div>
      <div className="review-card__body"><p>“{review.content}”</p></div>
    </article>
  );
}