from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GameInsightCreate(BaseModel):
    game_id: UUID
    total_reviews: int = Field(ge=0)
    average_rating: float = Field(ge=0, le=10)
    positive_percentage: float = Field(ge=0, le=100)
    neutral_percentage: float = Field(ge=0, le=100)
    negative_percentage: float = Field(ge=0, le=100)
    easy_percentage: float = Field(ge=0, le=100)
    medium_percentage: float = Field(ge=0, le=100)
    hard_percentage: float = Field(ge=0, le=100)
    generated_at: datetime | None = None


class GameInsightUpdate(BaseModel):
    game_id: UUID | None = None
    total_reviews: int | None = Field(default=None, ge=0)
    average_rating: float | None = Field(default=None, ge=0, le=10)
    positive_percentage: float | None = Field(default=None, ge=0, le=100)
    neutral_percentage: float | None = Field(default=None, ge=0, le=100)
    negative_percentage: float | None = Field(default=None, ge=0, le=100)
    easy_percentage: float | None = Field(default=None, ge=0, le=100)
    medium_percentage: float | None = Field(default=None, ge=0, le=100)
    hard_percentage: float | None = Field(default=None, ge=0, le=100)
    generated_at: datetime | None = None


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
