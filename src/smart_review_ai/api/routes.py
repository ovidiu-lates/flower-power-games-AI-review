from fastapi import APIRouter

from smart_review_ai.models import (
    GameInsights,
    Review,
    ReviewAnalysis,
)

router = APIRouter()


@router.post("/reviews/analyze", response_model=ReviewAnalysis)
def analyze_review(review: Review):
    return ReviewAnalysis(
        sentiment="positive",
        difficulty="medium",
        themes=["strategy"],
        complaints=[],
    )


@router.get(
    "/games/{game_id}/insights",
    response_model=GameInsights,
)
def get_game_insights(game_id: int):
    return GameInsights(
        game_id=game_id,
        review_count=100,
        positive_percentage=83.0,
        perceived_difficulty="medium-high",
        liked_aspects=[
            "strategic depth",
            "replayability",
            "player interaction",
        ],
        common_complaints=[
            "long setup time",
            "difficult first game",
            "rulebook clarity",
        ],
    )