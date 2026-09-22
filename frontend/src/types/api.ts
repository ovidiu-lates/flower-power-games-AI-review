export interface User {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
}

export interface Game {
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
}

export interface Review {
  id: string;
  user_id: string;
  game_id: string;
  rating: number;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface InsightItem {
  occurrence_count: number;
  percentage: number;
}

export interface LikedAspect extends InsightItem {
  aspect: string;
}

export interface Complaint extends InsightItem {
  complaint: string;
}

export interface GameInsight {
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
  liked_aspects: LikedAspect[];
  complaints: Complaint[];
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}