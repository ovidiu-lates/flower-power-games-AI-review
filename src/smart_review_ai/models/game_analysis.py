from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from smart_review_ai.db.database import Base


class GameAnalysis(Base):
    __tablename__ = "game_analysis"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id"),
        nullable=False,
    )

    review_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    positive_sentiment: Mapped[Decimal] = mapped_column(
        Numeric(5, 4),
        nullable=False,
    )

    neutral_sentiment: Mapped[Decimal] = mapped_column(
        Numeric(5, 4),
        nullable=False,
    )

    negative_sentiment: Mapped[Decimal] = mapped_column(
        Numeric(5, 4),
        nullable=False,
    )

    perceived_difficulty: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
