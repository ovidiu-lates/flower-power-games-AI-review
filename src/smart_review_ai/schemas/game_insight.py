from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GameInsightLikedAspectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    aspect: str
    occurrence_count: int
    percentage: float


class GameInsightComplaintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    complaint: str
    occurrence_count: int
    percentage: float


class GameInsightResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    game_id: UUID
    total_reviews: int
    average_rating: float
    positive_percentage: float
    neutral_percentage: float
    negative_percentage: float
    easy_percentage: float
    medium_percentage: float
    hard_percentage: float
    generated_at: datetime
    liked_aspects: list[GameInsightLikedAspectResponse]
    complaints: list[GameInsightComplaintResponse]


class GameInsightExplanationResponse(BaseModel):
    game_id: UUID
    review_count: int
    explanation: str
