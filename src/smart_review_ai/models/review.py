from pydantic import BaseModel


class Review(BaseModel):
    game_id: int
    text: str
