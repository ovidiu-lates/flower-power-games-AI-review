from uuid import UUID

from sqlalchemy.orm import Session

from smart_review_ai.analysis.review_analyzer import (
    ReviewAnalysisResult,
    ReviewAnalyzer,
    get_default_review_analyzer,
)
from smart_review_ai.core.exceptions import EntityNotFoundError
from smart_review_ai.models.review import Review
from smart_review_ai.models.review_analysis import ReviewAnalysis
from smart_review_ai.models.review_complaint import ReviewComplaint
from smart_review_ai.models.review_liked_aspect import ReviewLikedAspect
from smart_review_ai.repositories.game_repository import GameRepository
from smart_review_ai.repositories.review_repository import ReviewRepository
from smart_review_ai.services.game_insights_service import GameInsightsService


class ReviewService:
    def __init__(self, session: Session, analyzer: ReviewAnalyzer | None = None) -> None:
        self.session = session
        self.reviews = ReviewRepository(session)
        self.games = GameRepository(session)
        self.analyzer = analyzer if analyzer is not None else get_default_review_analyzer()

    def create_review(
        self, *, user_id: UUID, game_id: UUID, rating: int, content: str
    ) -> Review:
        self._require_game(game_id)
        review = self.reviews.create(
            user_id=user_id,
            game_id=game_id,
            rating=rating,
            content=content,
        )
        if self.analyzer is not None:
            analysis = self.analyzer.analyze(content=content, rating=rating)
            self._create_review_analysis(review, analysis)
            GameInsightsService(self.session).regenerate_game_insight(game_id)
        self.session.commit()
        return review

    def get_review(self, review_id: UUID) -> Review:
        review = self.reviews.get_by_id(review_id)
        if review is None:
            raise EntityNotFoundError("Review not found")
        return review

    def list_reviews_for_game(self, game_id: UUID) -> list[Review]:
        self._require_game(game_id)
        return self.reviews.list_by_game_id(game_id)

    def list_reviews_for_user(self, user_id: UUID) -> list[Review]:
        return self.reviews.list_by_user_id(user_id)

    def _require_game(self, game_id: UUID) -> None:
        if self.games.get_by_id(game_id) is None:
            raise EntityNotFoundError("Game not found")

    def _create_review_analysis(
        self, review: Review, result: ReviewAnalysisResult
    ) -> ReviewAnalysis:
        analysis = ReviewAnalysis(
            review=review,
            sentiment=result.sentiment,
            confidence=result.confidence,
            perceived_difficulty=result.perceived_difficulty,
        )
        analysis.liked_aspects.extend(
            ReviewLikedAspect(aspect=aspect) for aspect in result.liked_aspects
        )
        analysis.complaints.extend(
            ReviewComplaint(complaint=complaint) for complaint in result.complaints
        )
        self.session.add(analysis)
        self.session.flush()
        return analysis