from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from smart_review_ai.db.database import Base


class CommonComplaint(Base):
    __tablename__ = "common_complaints"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    game_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("game_analysis.id"),
        nullable=False,
    )

    complaint: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )