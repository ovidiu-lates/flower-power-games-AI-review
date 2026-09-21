from __future__ import annotations

from typing import Literal, Protocol

from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, field_validator

from smart_review_ai.core.config import settings

Sentiment = Literal["positive", "neutral", "negative"]
Difficulty = Literal["easy", "medium", "hard"]


class ReviewAnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sentiment: Sentiment
    confidence: float = Field(ge=0, le=1)
    perceived_difficulty: Difficulty
    liked_aspects: list[str] = Field(default_factory=list, max_length=5)
    complaints: list[str] = Field(default_factory=list, max_length=5)

    @field_validator("liked_aspects", "complaints")
    @classmethod
    def clean_items(cls, values: list[str]) -> list[str]:
        seen: set[str] = set()
        cleaned: list[str] = []
        for value in values:
            item = value.strip().lower()[:255]
            if item and item not in seen:
                cleaned.append(item)
                seen.add(item)
        return cleaned


class ReviewAnalyzer(Protocol):
    def analyze(self, *, content: str, rating: int) -> ReviewAnalysisResult: ...


class OpenAIReviewAnalyzer:
    def __init__(self, *, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def analyze(self, *, content: str, rating: int) -> ReviewAnalysisResult:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You analyze board game reviews. Return only valid JSON with "
                        "these exact keys: sentiment, confidence, "
                        "perceived_difficulty, liked_aspects, complaints. "
                        "sentiment must be one of positive, neutral, negative. "
                        "perceived_difficulty must be one of easy, medium, hard. "
                        "confidence must be a number between 0 and 1. "
                        "liked_aspects and complaints must be arrays of at most five "
                        "short lowercase strings. Use [] when none are present. "
                        "Normalize liked_aspects and complaints into canonical concepts "
                        "instead of copying the review wording. For example, map phrases "
                        "like 'great replay value', 'fun to play again', or 'never gets old' "
                        "to 'replayability'. Map similar complaints to one stable concept, "
                        "such as 'takes forever to set up' to 'long setup'. Prefer reusable "
                        "board game concepts like replayability, strategy, components, "
                        "theme, rules clarity, downtime, balance, player interaction, "
                        "setup time, and play time."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Rating: {rating}/10\n"
                        f"Review text:\n{content}\n\n"
                        "Analyze this review and return the JSON object."
                    ),
                },
            ],
        )
        message = response.choices[0].message.content
        if message is None:
            raise ValueError("OpenAI returned an empty review analysis response")
        return ReviewAnalysisResult.model_validate_json(message)


def get_default_review_analyzer() -> ReviewAnalyzer | None:
    if settings.openai_api_key is None:
        return None
    return OpenAIReviewAnalyzer(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )