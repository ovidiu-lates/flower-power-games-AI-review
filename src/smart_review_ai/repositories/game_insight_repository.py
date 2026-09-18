from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from smart_review_ai.models.game_insight import GameInsight


class GameInsightRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, insight_id: UUID) -> GameInsight | None:
        return self.session.get(GameInsight, insight_id)

    def list(self) -> list[GameInsight]:
        statement = select(GameInsight).order_by(GameInsight.generated_at.desc())
        return list(self.session.scalars(statement))

    def create(self, **values: object) -> GameInsight:
        insight = GameInsight(**values)
        self.session.add(insight)
        self.session.flush()
        self.session.refresh(insight)
        return insight

    def update(self, insight: GameInsight, values: dict[str, object]) -> GameInsight:
        for field, value in values.items():
            setattr(insight, field, value)
        self.session.flush()
        self.session.refresh(insight)
        return insight

    def delete(self, insight: GameInsight) -> None:
        self.session.delete(insight)
        self.session.flush()
