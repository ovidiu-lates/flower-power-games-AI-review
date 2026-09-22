from collections import Counter
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from smart_review_ai.analysis.game_insight_explainer import (
    GameInsightExplainer,
    get_default_game_insight_explainer,
)
from smart_review_ai.core.exceptions import EntityNotFoundError, ServiceUnavailableError
from smart_review_ai.models.game_insight import GameInsight
from smart_review_ai.models.game_insight_complaint import GameInsightComplaint
from smart_review_ai.models.game_insight_liked_aspect import GameInsightLikedAspect
from smart_review_ai.models.review import Review
from smart_review_ai.models.review_analysis import ReviewAnalysis
from smart_review_ai.repositories.game_insight_repository import GameInsightRepository
from smart_review_ai.repositories.game_repository import GameRepository


class GameInsightsService:
    def __init__(
        self, session: Session, explainer: GameInsightExplainer | None = None
    ) -> None:
        self.session = session
        self.insights = GameInsightRepository(session)
        self.games = GameRepository(session)
        self.explainer = (
            explainer if explainer is not None else get_default_game_insight_explainer()
        )

    def get_game_insight(self, game_id: UUID) -> GameInsight:
        self._require_game(game_id)
        insight = self.insights.get_latest_by_game_id(game_id)
        if insight is None:
            raise EntityNotFoundError("Game insight not found")
        return insight

    def regenerate_game_insight(self, game_id: UUID) -> GameInsight:
        self._require_game(game_id)
        reviews = self._list_analyzed_reviews(game_id)
        total_reviews = len(reviews)

        insight = self.insights.get_latest_by_game_id(game_id)
        values = {
            "total_reviews": total_reviews,
            "average_rating": self._average_rating(reviews),
            "positive_percentage": self._percentage_for(
                reviews, "sentiment", "positive"
            ),
            "neutral_percentage": self._percentage_for(reviews, "sentiment", "neutral"),
            "negative_percentage": self._percentage_for(
                reviews, "sentiment", "negative"
            ),
            "easy_percentage": self._percentage_for(
                reviews, "perceived_difficulty", "easy"
            ),
            "medium_percentage": self._percentage_for(
                reviews, "perceived_difficulty", "medium"
            ),
            "hard_percentage": self._percentage_for(
                reviews, "perceived_difficulty", "hard"
            ),
        }
        if insight is None:
            insight = self.insights.create(game_id=game_id, **values)
        else:
            for field, value in values.items():
                setattr(insight, field, value)
            insight.generated_at = datetime.now(UTC)
            insight.liked_aspects.clear()
            insight.complaints.clear()
        insight.liked_aspects.extend(
            GameInsightLikedAspect(
                aspect=aspect,
                occurrence_count=count,
                percentage=self._percentage(count, total_reviews),
            )
            for aspect, count in self._count_liked_aspects(reviews).most_common(5)
        )
        insight.complaints.extend(
            GameInsightComplaint(
                complaint=complaint,
                occurrence_count=count,
                percentage=self._percentage(count, total_reviews),
            )
            for complaint, count in self._count_complaints(reviews).most_common(5)
        )
        self.session.flush()
        self.session.refresh(insight)
        return insight

    def explain_game_insight(self, game_id: UUID, review_limit: int) -> tuple[str, int]:
        game = self.games.get_by_id(game_id)
        if game is None:
            raise EntityNotFoundError("Game not found")
        insight = self.get_game_insight(game_id)
        if self.explainer is None:
            raise ServiceUnavailableError("OpenAI API key is not configured")
        reviews = self._list_recent_reviews(game_id, review_limit)
        explanation = self.explainer.explain(
            game_name=game.name,
            insight=insight,
            reviews=reviews,
        )
        return explanation, len(reviews)

    def _require_game(self, game_id: object) -> None:
        if not isinstance(game_id, UUID) or self.games.get_by_id(game_id) is None:
            raise EntityNotFoundError("Game not found")

    def _list_analyzed_reviews(self, game_id: UUID) -> list[Review]:
        statement = (
            select(Review)
            .options(
                selectinload(Review.analysis).selectinload(
                    ReviewAnalysis.liked_aspects
                ),
                selectinload(Review.analysis).selectinload(ReviewAnalysis.complaints),
            )
            .where(Review.game_id == game_id, Review.analysis.has())
        )
        return list(self.session.scalars(statement))

    def _list_recent_reviews(self, game_id: UUID, limit: int) -> list[Review]:
        statement = (
            select(Review)
            .where(Review.game_id == game_id)
            .order_by(Review.created_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(statement))

    @staticmethod
    def _average_rating(reviews: list[Review]) -> float:
        if not reviews:
            return 0.0
        return sum(review.rating for review in reviews) / len(reviews)

    @classmethod
    def _percentage_for(
        cls, reviews: list[Review], attribute: str, expected_value: str
    ) -> float:
        count = sum(
            1
            for review in reviews
            if review.analysis is not None
            and getattr(review.analysis, attribute) == expected_value
        )
        return cls._percentage(count, len(reviews))

    @staticmethod
    def _percentage(count: int, total: int) -> float:
        if total == 0:
            return 0.0
        return (count / total) * 100

    @staticmethod
    def _count_liked_aspects(reviews: list[Review]) -> Counter[str]:
        counter: Counter[str] = Counter()
        for review in reviews:
            if review.analysis is not None:
                counter.update(aspect.aspect for aspect in review.analysis.liked_aspects)
        return counter

    @staticmethod
    def _count_complaints(reviews: list[Review]) -> Counter[str]:
        counter: Counter[str] = Counter()
        for review in reviews:
            if review.analysis is not None:
                counter.update(complaint.complaint for complaint in review.analysis.complaints)
        return counter