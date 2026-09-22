import { ArrowRight, Clock3, Search, UsersRound } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import GameArtwork from "../components/GameArtwork";
import { listGames } from "../services/gameService";
import type { Game } from "../types/api";

export default function DiscoverPage() {
  const [params] = useSearchParams();
  const search = params.get("search") ?? "";
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true); setError("");
    listGames(search).then((response) => setGames(response.items)).catch((caught) => setError(caught instanceof Error ? caught.message : "Could not load games.")).finally(() => setLoading(false));
  }, [search]);

  return (
    <main className="page-shell discover-page">
      <header className="discover-header"><span className="eyebrow">The game shelf</span><h1>{search ? `Results for “${search}”` : "Find your next table favorite"}</h1><p>Browse the catalog, then use player-backed AI insights to make the call.</p></header>
      {loading && <div className="state-message"><span className="loader" /> Loading games...</div>}
      {error && <div className="state-message state-message--error">{error}</div>}
      {!loading && !error && games.length === 0 && <div className="state-message"><Search size={24} /> No games match this search.</div>}
      <div className="game-grid">{games.map((game) => <Link to={`/games/${game.id}`} className="game-card" key={game.id}><div className="game-card__image"><GameArtwork src={game.image_url} name={game.name} /><span>View game <ArrowRight size={15} /></span></div><div className="game-card__content"><h2>{game.name}</h2><p>{game.description}</p><div><span><UsersRound size={15} /> {game.min_players}-{game.max_players}</span><span><Clock3 size={15} /> {game.min_play_time}-{game.max_play_time} min</span></div></div></Link>)}</div>
    </main>
  );
}