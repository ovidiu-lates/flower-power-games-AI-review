from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from smart_review_ai.models.review import Review


class ReviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, review_id: UUID) -> Review | None:
        return self.session.get(Review, review_id)

    def list(self) -> list[Review]:
        statement = select(Review).order_by(Review.created_at.desc())
        return list(self.session.scalars(statement))

    def list_by_game_id(self, game_id: UUID) -> list[Review]:
        statement = (
            select(Review)
            .where(Review.game_id == game_id)
            .order_by(Review.created_at.desc())
        )
        return list(self.session.scalars(statement))

    def list_by_user_id(self, user_id: UUID) -> list[Review]:
        statement = (
            select(Review)
            .where(Review.user_id == user_id)
            .order_by(Review.created_at.desc())
        )
        return list(self.session.scalars(statement))

    def create(self, **values: object) -> Review:
        review = Review(**values)
        self.session.add(review)
        self.session.flush()
        self.session.refresh(review)
        return review