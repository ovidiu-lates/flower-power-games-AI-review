export type Difficulty = "easy" | "medium" | "hard";
export type Sentiment = "positive" | "mixed" | "neutral" | "negative";

export type Game = {
  id: string;
  name: string;
  description: string;
  image_url: string;
  min_players: number;
  max_players: number;
  min_play_time: number;
  max_play_time: number;
  created_at: string;
  updated_at: string;
};

export type GameInsightAspect = {
  aspect: string;
  occurrence_count: number;
  percentage: number;
};

export type GameInsightComplaint = {
  complaint: string;
  occurrence_count: number;
  percentage: number;
};

export type GameInsight = {
  id: string;
  game_id: string;
  total_reviews: number;
  average_rating: number;
  positive_percentage: number;
  neutral_percentage: number;
  negative_percentage: number;
  easy_percentage: number;
  medium_percentage: number;
  hard_percentage: number;
  generated_at: string;
  liked_aspects: GameInsightAspect[];
  complaints: GameInsightComplaint[];
};

export type Review = {
  id: string;
  user_id: string;
  game_id: string;
  rating: number;
  content: string;
  created_at: string;
  updated_at: string;
};

export type User = {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type GameCardGame = {
  id: string;
  title: string;
  description: string;
  coverImage: string;
  minPlayers: number;
  maxPlayers: number;
  minPlayTime: number;
  maxPlayTime: number;
  rating: number | null;
  reviewCount: number | null;
  positivePct: number | null;
  difficulty: Difficulty | null;
  tags: string[];
  insightsGeneratedAt: string | null;
};

export type PaginatedGamesResponse = {
  items: Game[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
};