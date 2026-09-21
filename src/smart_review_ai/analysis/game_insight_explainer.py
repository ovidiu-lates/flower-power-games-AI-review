from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from openai import OpenAI

from smart_review_ai.core.config import settings

if TYPE_CHECKING:
    from smart_review_ai.models.game_insight import GameInsight
    from smart_review_ai.models.review import Review


class GameInsightExplainer(Protocol):
    def explain(
        self, *, game_name: str, insight: GameInsight, reviews: list[Review]
    ) -> str: ...


class OpenAIGameInsightExplainer:
    def __init__(self, *, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def explain(
        self, *, game_name: str, insight: GameInsight, reviews: list[Review]
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You explain board game review insights to app users. "
                        "Write a concise, balanced explanation of the overall user "
                        "opinion. Base the explanation only on the supplied aggregate "
                        "insight and review samples. Mention the main positives, main "
                        "complaints, perceived difficulty, and rating trend when useful. "
                        "Do not invent facts. Keep it to one short paragraph."
                    ),
                },
                {
                    "role": "user",
                    "content": self._build_prompt(game_name, insight, reviews),
                },
            ],
        )
        message = response.choices[0].message.content
        if message is None:
            raise ValueError("OpenAI returned an empty game insight explanation")
        return message.strip()

    def _build_prompt(
        self, game_name: str, insight: GameInsight, reviews: list[Review]
    ) -> str:
        liked_aspects = ", ".join(
            f"{item.aspect} ({item.percentage:.1f}%)"
            for item in insight.liked_aspects
        ) or "none"
        complaints = ", ".join(
            f"{item.complaint} ({item.percentage:.1f}%)"
            for item in insight.complaints
        ) or "none"
        review_samples = "\n".join(
            f"- Rating {review.rating}/10: {review.content}" for review in reviews
        ) or "No review samples were provided."
        return (
            f"Game: {game_name}\n"
            f"Total analyzed reviews: {insight.total_reviews}\n"
            f"Average rating: {insight.average_rating:.1f}/10\n"
            "Sentiment: "
            f"{insight.positive_percentage:.1f}% positive, "
            f"{insight.neutral_percentage:.1f}% neutral, "
            f"{insight.negative_percentage:.1f}% negative\n"
            "Perceived difficulty: "
            f"{insight.easy_percentage:.1f}% easy, "
            f"{insight.medium_percentage:.1f}% medium, "
            f"{insight.hard_percentage:.1f}% hard\n"
            f"Liked aspects: {liked_aspects}\n"
            f"Complaints: {complaints}\n"
            f"Review samples:\n{review_samples}"
        )


def get_default_game_insight_explainer() -> GameInsightExplainer | None:
    if settings.openai_api_key is None:
        return None
    return OpenAIGameInsightExplainer(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )