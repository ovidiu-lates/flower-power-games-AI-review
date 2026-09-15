from pydantic import BaseModel


class ReviewAnalysis(BaseModel):
    sentiment: str
    difficulty: str | None = None
    themes: list[str] = []
    complaints: list[str] = []
