import { useEffect, useState } from "react";
import ReviewCard from "../components/ReviewCard";
import { getMyReviews } from "../lib/gamesApi";
import type { UserReview } from "../types/game";

export default function MyReviews() {
  const [reviews, setReviews] = useState<UserReview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getMyReviews()
      .then(setReviews)
      .catch((caught) => setError(caught instanceof Error ? caught.message : "Could not load your reviews."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="page-shell my-reviews-page">
      <header className="page-heading">
        <span className="eyebrow">Your voice in the community</span>
        <h1>My reviews</h1>
        <p>Reviews you have shared with fellow players.</p>
      </header>

      {loading && <div className="state-message"><span className="loader" /> Loading your reviews...</div>}
      {!loading && error && <div className="state-message state-message--error">{error}</div>}
      {!loading && !error && reviews.length === 0 && (
        <div className="panel state-message"><p>You have not written any reviews yet.</p></div>
      )}
      {!loading && !error && reviews.length > 0 && (
        <div className="review-list">
          {reviews.map((review) => (
            <ReviewCard
              key={review.id}
              review={review}
              gameName={review.game_name}
              gameImageUrl={review.game_image_url}
            />
          ))}
        </div>
      )}
    </main>
  );
}
