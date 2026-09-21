from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from smart_review_ai.db.database import Base

if TYPE_CHECKING:
    from smart_review_ai.models.game import Game
    from smart_review_ai.models.review_analysis import ReviewAnalysis
    from smart_review_ai.models.user import User


class Review(Base):
    __tablename__ = "review"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user.id"),
        nullable=False,
    )
    game_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("game.id"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="reviews")
    game: Mapped[Game] = relationship(back_populates="reviews")
    analysis: Mapped[ReviewAnalysis | None] = relationship(
        back_populates="review",
        uselist=False,
        cascade="all, delete-orphan",
    )
