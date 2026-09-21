from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from smart_review_ai.models.game_insight import GameInsight


class GameInsightRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, insight_id: UUID) -> GameInsight | None:
        return self.session.get(GameInsight, insight_id)

    def get_latest_by_game_id(self, game_id: UUID) -> GameInsight | None:
        statement = (
            select(GameInsight)
            .options(
                selectinload(GameInsight.liked_aspects),
                selectinload(GameInsight.complaints),
            )
            .where(GameInsight.game_id == game_id)
            .order_by(GameInsight.generated_at.desc())
            .limit(1)
        )
        return self.session.scalar(statement)

    def list(self) -> list[GameInsight]:
        statement = select(GameInsight).order_by(GameInsight.generated_at.desc())
        return list(self.session.scalars(statement))

    def create(self, **values: object) -> GameInsight:
        insight = GameInsight(**values)
        self.session.add(insight)
        self.session.flush()
        self.session.refresh(insight)
        return insight

