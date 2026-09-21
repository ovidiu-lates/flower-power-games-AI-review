from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from smart_review_ai.db.database import Base

if TYPE_CHECKING:
    from smart_review_ai.models.game_insight import GameInsight


class GameInsightLikedAspect(Base):
    __tablename__ = "game_insight_liked_aspect"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    game_insight_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("game_insight.id"), nullable=False
    )
    aspect: Mapped[str] = mapped_column(String(255), nullable=False)
    occurrence_count: Mapped[int] = mapped_column(Integer, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, nullable=False)

    game_insight: Mapped[GameInsight] = relationship(back_populates="liked_aspects")
