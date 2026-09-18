from uuid import UUID

from sqlalchemy.orm import Session

from smart_review_ai.core.exceptions import EntityNotFoundError
from smart_review_ai.models.review import Review
from smart_review_ai.repositories.game_repository import GameRepository
from smart_review_ai.repositories.review_repository import ReviewRepository


class ReviewService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.reviews = ReviewRepository(session)
        self.games = GameRepository(session)

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
        self.session.commit()
        return review

    def get_review(self, review_id: UUID) -> Review:
        review = self.reviews.get_by_id(review_id)
        if review is None:
            raise EntityNotFoundError("Review not found")
        return review

    def list_reviews(self) -> list[Review]:
        return self.reviews.list()

    def update_review(self, review_id: UUID, values: dict[str, object]) -> Review:
        review = self.get_review(review_id)
        game_id = values.get("game_id")
        if isinstance(game_id, UUID):
            self._require_game(game_id)
        review = self.reviews.update(review, values)
        self.session.commit()
        return review

    def delete_review(self, review_id: UUID) -> None:
        review = self.get_review(review_id)
        self.reviews.delete(review)
        self.session.commit()

    def _require_game(self, game_id: UUID) -> None:
        if self.games.get_by_id(game_id) is None:
            raise EntityNotFoundError("Game not found")
