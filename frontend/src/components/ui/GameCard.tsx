import type { GameCardGame } from "../../types/game";
import { DifficultyBadge, Tag } from "./Badges";

export default function GameCard({ game }: { game: GameCardGame }) {
	const rating = game.rating === null ? "--" : game.rating.toFixed(1);
	const reviewCount = game.reviewCount === null ? "No analyzed reviews" : `${game.reviewCount.toLocaleString()} analyzed reviews`;
	const positivePct = game.positivePct === null ? null : Math.round(game.positivePct);

	return (
		<article className="game-card">
			<div className="game-card-cover">
				<img src={game.coverImage} alt={game.title} />
				<div className="game-card-difficulty">
					<DifficultyBadge difficulty={game.difficulty} />
				</div>
				<div className="game-card-cover-gradient" />
				<div className="game-card-rating">
					<span>{rating}</span>
					<small>/ 5</small>
				</div>
			</div>

			<div className="game-card-content">
				<div>
					<h3>{game.title}</h3>
					<p>{reviewCount}</p>
				</div>

				<div className="game-card-meta">
					<span>{game.minPlayers}-{game.maxPlayers} players</span>
					<span>{game.minPlayTime}-{game.maxPlayTime} min</span>
				</div>

				{positivePct === null ? (
					<p className="game-card-no-insight">AI insight has not been generated yet.</p>
				) : (
					<div className="sentiment-row">
						<div className="sentiment-bar" aria-hidden="true">
							<div style={{ width: `${positivePct}%` }} />
						</div>
						<span>{positivePct}% positive</span>
					</div>
				)}

				{game.tags.length > 0 && (
					<div className="game-card-tags">
						{game.tags.map((tag) => (
							<Tag key={tag} label={tag} />
						))}
					</div>
				)}

				<div className="game-card-footer">
					<span>View insights →</span>
				</div>
			</div>
		</article>
	);
}
