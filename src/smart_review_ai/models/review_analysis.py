from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from smart_review_ai.db.database import Base

if TYPE_CHECKING:
    from smart_review_ai.models.review import Review
    from smart_review_ai.models.review_complaint import ReviewComplaint
    from smart_review_ai.models.review_liked_aspect import ReviewLikedAspect


class ReviewAnalysis(Base):
    __tablename__ = "review_analysis"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    review_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("review.id"), unique=True, nullable=False
    )
    sentiment: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    perceived_difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    review: Mapped[Review] = relationship(back_populates="analysis")
    liked_aspects: Mapped[list[ReviewLikedAspect]] = relationship(
        back_populates="review_analysis", cascade="all, delete-orphan"
    )
    complaints: Mapped[list[ReviewComplaint]] = relationship(
        back_populates="review_analysis", cascade="all, delete-orphan"
    )
