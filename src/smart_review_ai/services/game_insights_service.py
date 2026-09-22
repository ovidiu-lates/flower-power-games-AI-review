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

    def get_game_insight(self, game_id: UUID) -> GameInsight:
        self._require_game(game_id)
        insight = self.insights.get_latest_by_game_id(game_id)
        if insight is None:
            raise EntityNotFoundError("Game insight not found")
        return insight

    def _require_game(self, game_id: object) -> None:
        if not isinstance(game_id, UUID) or self.games.get_by_id(game_id) is None:
            raise EntityNotFoundError("Game not found")
