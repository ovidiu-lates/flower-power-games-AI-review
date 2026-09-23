from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from smart_review_ai.db.database import Base
from smart_review_ai.models.game_insight_complaint import GameInsightComplaint
from smart_review_ai.models.game_insight_liked_aspect import GameInsightLikedAspect

if TYPE_CHECKING:
    from smart_review_ai.models.game import Game
    from smart_review_ai.models.game_insight_complaint import GameInsightComplaint
    from smart_review_ai.models.game_insight_liked_aspect import GameInsightLikedAspect


class GameInsight(Base):
    __tablename__ = "game_insight"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    game_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("game.id"), nullable=False
    )
    total_reviews: Mapped[int] = mapped_column(Integer, nullable=False)
    average_rating: Mapped[float] = mapped_column(Float, nullable=False)
    positive_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    neutral_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    negative_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    easy_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    medium_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    hard_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    game: Mapped[Game] = relationship(back_populates="insights")
    liked_aspects: Mapped[list[GameInsightLikedAspect]] = relationship(
        back_populates="game_insight",
        cascade="all, delete-orphan",
        order_by=lambda: (
            GameInsightLikedAspect.occurrence_count.desc(),
            GameInsightLikedAspect.aspect.asc(),
        ),
    )
    complaints: Mapped[list[GameInsightComplaint]] = relationship(
        back_populates="game_insight",
        cascade="all, delete-orphan",
        order_by=lambda: (
            GameInsightComplaint.occurrence_count.desc(),
            GameInsightComplaint.complaint.asc(),
        ),
    )
