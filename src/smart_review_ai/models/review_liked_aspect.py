from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from smart_review_ai.db.database import Base

if TYPE_CHECKING:
    from smart_review_ai.models.review_analysis import ReviewAnalysis


class ReviewLikedAspect(Base):
    __tablename__ = "review_liked_aspect"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    review_analysis_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("review_analysis.id"), nullable=False
    )
    aspect: Mapped[str] = mapped_column(String(255), nullable=False)

    review_analysis: Mapped[ReviewAnalysis] = relationship(
        back_populates="liked_aspects"
    )
