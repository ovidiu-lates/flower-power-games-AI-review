import type { Game, GameInsight, PaginatedResponse, Review } from "../types/api";
import { apiRequest } from "../lib/api";

export function listGames(search = "") {
  const query = new URLSearchParams({ page: "1", page_size: "24" });
  if (search.trim()) query.set("search", search.trim());
  return apiRequest<PaginatedResponse<Game>>(`/games?${query}`);
}

export function getGame(gameId: string) {
  return apiRequest<Game>(`/games/${gameId}`);
}

export async function getGameReviews(gameId: string, page = 1, pageSize = 5) {
  const query = new URLSearchParams({ page: String(page), page_size: String(pageSize) });
  const response = await apiRequest<PaginatedResponse<Review> | Review[]>(
    `/games/${gameId}/reviews?${query}`,
  );

  if (Array.isArray(response)) {
    const start = (page - 1) * pageSize;
    return {
      items: response.slice(start, start + pageSize),
      page,
      page_size: pageSize,
      total: response.length,
      total_pages: Math.max(1, Math.ceil(response.length / pageSize)),
    } satisfies PaginatedResponse<Review>;
  }
  return response;
}

export function getGameInsight(gameId: string) {
  return apiRequest<GameInsight>(`/games/${gameId}/insight`);
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