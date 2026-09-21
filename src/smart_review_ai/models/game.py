from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from smart_review_ai.db.database import Base

if TYPE_CHECKING:
    from smart_review_ai.models.game_insight import GameInsight
    from smart_review_ai.models.review import Review


class Game(Base):
    __tablename__ = "game"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    min_players: Mapped[int] = mapped_column(nullable=False)
    max_players: Mapped[int] = mapped_column(nullable=False)
    min_play_time: Mapped[int] = mapped_column(nullable=False)
    max_play_time: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    reviews: Mapped[list[Review]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )
    insights: Mapped[list[GameInsight]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )
