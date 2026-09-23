import type {
  Difficulty,
  Game,
  GameInsight,
  PaginatedGamesResponse,
  Review,
  UserReview,
} from "../types/game";
import { apiRequest, ApiError } from "./api";

type GetGamesParams = {
  search?: string;
  players?: string;
  maxTime?: string;
  difficulty?: Difficulty | "";
  sort?: "rating" | "name";
  token?: string;
};

export async function getGames({
  search,
  players,
  maxTime,
  difficulty,
  sort,
  token: _token,
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

  return apiRequest<PaginatedGamesResponse>(`/games?${params.toString()}`);
}

export function getGame(gameId: string) {
  return apiRequest<Game>(`/games/${gameId}`);
}

export async function getGameInsight(
  gameId: string,
  _token?: string,
): Promise<GameInsight | null> {
  try {
    return await apiRequest<GameInsight>(`/games/${gameId}/insight`);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return null;
    }
    throw error;
  }
}

export async function getGameReviews(gameId: string, page = 1, pageSize = 5) {
  const query = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
  });
  const response = await apiRequest<
    { items: Review[]; page: number; page_size: number; total: number; total_pages: number } | Review[]
  >(`/games/${gameId}/reviews?${query}`);

  if (!Array.isArray(response)) {
    return response;
  }

  const start = (page - 1) * pageSize;
  return {
    items: response.slice(start, start + pageSize),
    page,
    page_size: pageSize,
    total: response.length,
    total_pages: Math.max(1, Math.ceil(response.length / pageSize)),
  };
}

export function getMyReviews() {
  return apiRequest<UserReview[]>("/reviews/mine");
}

export function explainGameInsight(gameId: string, reviewCount: number) {
  const query = new URLSearchParams({ review_count: String(reviewCount) });
  return apiRequest<{ explanation: string }>(
    `/games/${gameId}/insight/explanation?${query}`,
    { method: "POST" },
  );
}

export function createReview(gameId: string, rating: number, content: string) {
  return apiRequest<Review>(`/games/${gameId}/reviews`, {
    method: "POST",
    body: JSON.stringify({ rating, content }),
  });
}
