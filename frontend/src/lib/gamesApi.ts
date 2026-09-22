import type { Difficulty, GameInsight, PaginatedGamesResponse, Review } from "../types/game";

type GetGamesParams = {
  search?: string;
  players?: string;
  maxTime?: string;
  difficulty?: Difficulty | "";
  sort?: "rating" | "name";
  token?: string;
};

function authHeaders(token?: string): HeadersInit | undefined {
  return token ? { Authorization: `Bearer ${token}` } : undefined;
}

export async function getGames({
  search,
  players,
  maxTime,
  difficulty,
  sort,
  token,
}: GetGamesParams): Promise<PaginatedGamesResponse> {
  const params = new URLSearchParams({
    page: "1",
    page_size: "50",
  });

  if (search) params.set("search", search);
  if (players) params.set("min_players", players);
  if (maxTime) params.set("max_play_time", maxTime);
  if (difficulty) params.set("difficulty", difficulty);

  if (sort === "rating") params.set("sort", "top_rated");

  const response = await fetch(`/api/games?${params.toString()}`, {
    headers: authHeaders(token),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch games: ${response.status}`);
  }

  return response.json();
}

export async function getGameInsight(
  gameId: string,
  token?: string,
): Promise<GameInsight | null> {
  const response = await fetch(`/api/games/${gameId}/insight`, {
    headers: authHeaders(token),
  });

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Failed to fetch game insight: ${response.status}`);
  }

  return response.json();
}

export async function getGameReviews(gameId: string, token?: string): Promise<Review[]> {
  const response = await fetch(`/api/games/${gameId}/reviews`, {
    headers: authHeaders(token),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch game reviews: ${response.status}`);
  }

  return response.json();
}