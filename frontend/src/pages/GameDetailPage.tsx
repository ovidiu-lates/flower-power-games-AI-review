import { ArrowLeft, ChevronLeft, ChevronRight, PenLine } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import GameArtwork from "../components/GameArtwork";
import InsightsPanel from "../components/InsightsPanel";
import ReviewCard from "../components/ReviewCard";
import WriteReviewModal from "../components/WriteReviewModal";
import { getGame, getGameInsight, getGameReviews } from "../services/gameService";
import type { Game, GameInsight, PaginatedResponse, Review } from "../types/api";

export default function GameDetailPage() {
  const { gameId = "" } = useParams();
  const [game, setGame] = useState<Game | null>(null);
  const [insight, setInsight] = useState<GameInsight | null>(null);
  const [reviews, setReviews] = useState<PaginatedResponse<Review> | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reviewOpen, setReviewOpen] = useState(false);

  useEffect(() => {
    setLoading(true); setError("");
    Promise.all([getGame(gameId), getGameReviews(gameId, page), getGameInsight(gameId).catch(() => null)])
      .then(([gameResponse, reviewResponse, insightResponse]) => { setGame(gameResponse); setReviews(reviewResponse); setInsight(insightResponse); })
      .catch((caught) => setError(caught instanceof Error ? caught.message : "Could not load this game."))
      .finally(() => setLoading(false));
  }, [gameId, page]);

  function refreshAfterReview() {
    setReviewOpen(false);
    setPage(1);
    void Promise.all([
      getGameReviews(gameId, 1),
      getGameInsight(gameId).catch(() => null),
    ]).then(([reviewResponse, insightResponse]) => {
      setReviews(reviewResponse);
      setInsight(insightResponse);
    });
  }

  if (loading && !game) return <main className="page-shell state-message"><span className="loader" /> Setting up the table...</main>;
  if (error || !game) return <main className="page-shell state-message state-message--error">{error || "Game not found."}<Link to="/discover">Back to discover</Link></main>;

  return (
    <main className="game-page">
      <header className="game-hero">
        <div className="game-hero__inner">
          <div className="game-hero__content">
            <div className="cover"><GameArtwork src={game.image_url} name={game.name} /></div>
            <div className="game-title">
              <Link className="back-link" to="/discover"><ArrowLeft size={14} /> Back to discover</Link>
              <div className="game-title__top">
                <div><h1>{game.name}</h1><p>{game.description}</p></div>
                <button className="button button--primary hero-review" onClick={() => setReviewOpen(true)}><PenLine size={16} /> Write a review</button>
              </div>
              <div className="stat-grid">
                <StatChip label="Rating" value={insight ? insight.average_rating.toFixed(1) : "—"} suffix="/10" />
                <StatChip label="Reviews analyzed" value={insight?.total_reviews.toLocaleString() ?? "0"} />
                <StatChip label="Players" value={`${game.min_players}–${game.max_players}`} />
                <StatChip label="Play time" value={`${game.min_play_time}–${game.max_play_time}`} suffix="min" />
              </div>
            </div>
          </div>
        </div>
      </header>
      <div className="game-content"><div className="game-content__main">
        {insight ? <InsightsPanel insight={insight} /> : <section className="panel empty-insight"><h2>Insights are still gathering</h2><p>There is not enough analyzed review data for this game yet.</p></section>}
        <section className="reviews-section"><div className="section-heading"><div><span className="eyebrow">From the community</span><h2>Player reviews</h2></div><button className="button button--secondary" onClick={() => setReviewOpen(true)}><PenLine size={16} /> Add yours</button></div><div className="review-list">{reviews?.items.map((review) => <ReviewCard review={review} key={review.id} />)}{reviews?.items.length === 0 && <div className="state-message">No reviews yet. Start the conversation.</div>}</div>{reviews && reviews.total_pages > 1 && <nav className="pagination" aria-label="Review pages"><button className="icon-button" disabled={page === 1} onClick={() => setPage((value) => value - 1)} aria-label="Previous page"><ChevronLeft /></button><span>Page {reviews.page} of {reviews.total_pages}</span><button className="icon-button" disabled={page === reviews.total_pages} onClick={() => setPage((value) => value + 1)} aria-label="Next page"><ChevronRight /></button></nav>}</section>
      </div><aside className="game-aside"><section className="panel quick-facts"><span className="eyebrow">At a glance</span><h2>Game details</h2><dl><div><dt>Players</dt><dd>{game.min_players}-{game.max_players}</dd></div><div><dt>Play time</dt><dd>{game.min_play_time}-{game.max_play_time} min</dd></div><div><dt>Community rating</dt><dd>{insight ? `${insight.average_rating.toFixed(1)}/10` : "Pending"}</dd></div><div><dt>Reviews analyzed</dt><dd>{insight?.total_reviews.toLocaleString() ?? "0"}</dd></div></dl></section><section className="review-cta"><PenLine size={23} /><h2>Played this one?</h2><p>Add your experience to sharpen the community insight.</p><button className="button button--light" onClick={() => setReviewOpen(true)}>Write a review</button></section></aside></div>
      {reviewOpen && <WriteReviewModal gameId={game.id} gameName={game.name} onClose={() => setReviewOpen(false)} onCreated={refreshAfterReview} />}
    </main>
  );
}

function StatChip({ label, value, suffix }: { label: string; value: string; suffix?: string }) {
  return <div className="stat-chip"><div><strong>{value}</strong>{suffix && <span>{suffix}</span>}</div><small>{label}</small></div>;
}