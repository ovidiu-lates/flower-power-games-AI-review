# models/game_insights.py
from pydantic import BaseModel


class GameInsights(BaseModel):
    game_id: int
    review_count: int
    positive_percentage: float
    perceived_difficulty: str
    liked_aspects: list[str]
    common_complaints: list[str]
