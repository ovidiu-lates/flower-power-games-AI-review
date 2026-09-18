from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GameCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str
    image_url: str = Field(max_length=2048)
    min_players: int = Field(ge=1)
    max_players: int = Field(ge=1)
    min_play_time: int = Field(ge=0)
    max_play_time: int = Field(ge=0)


class GameUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    image_url: str | None = Field(default=None, max_length=2048)
    min_players: int | None = Field(default=None, ge=1)
    max_players: int | None = Field(default=None, ge=1)
    min_play_time: int | None = Field(default=None, ge=0)
    max_play_time: int | None = Field(default=None, ge=0)


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    image_url: str
    min_players: int
    max_players: int
    min_play_time: int
    max_play_time: int
    created_at: datetime
    updated_at: datetime
