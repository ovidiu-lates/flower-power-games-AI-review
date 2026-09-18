from uuid import UUID

from sqlalchemy.orm import Session

from smart_review_ai.core.exceptions import EntityNotFoundError
from smart_review_ai.models.game_insight import GameInsight
from smart_review_ai.repositories.game_insight_repository import GameInsightRepository
from smart_review_ai.repositories.game_repository import GameRepository


class GameInsightsService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.insights = GameInsightRepository(session)
        self.games = GameRepository(session)

    def create_game_insights(self, **values: object) -> GameInsight:
        self._require_game(values["game_id"])
        insight = self.insights.create(**values)
        self.session.commit()
        return insight

    def get_game_insights(self, insight_id: UUID) -> GameInsight:
        insight = self.insights.get_by_id(insight_id)
        if insight is None:
            raise EntityNotFoundError("Game insights not found")
        return insight

    def list_game_insights(self) -> list[GameInsight]:
        return self.insights.list()

    def update_game_insights(
        self, insight_id: UUID, values: dict[str, object]
    ) -> GameInsight:
        insight = self.get_game_insights(insight_id)
        game_id = values.get("game_id")
        if isinstance(game_id, UUID):
            self._require_game(game_id)
        insight = self.insights.update(insight, values)
        self.session.commit()
        return insight

    def delete_game_insights(self, insight_id: UUID) -> None:
        insight = self.get_game_insights(insight_id)
        self.insights.delete(insight)
        self.session.commit()

    def _require_game(self, game_id: object) -> None:
        if not isinstance(game_id, UUID) or self.games.get_by_id(game_id) is None:
            raise EntityNotFoundError("Game not found")
