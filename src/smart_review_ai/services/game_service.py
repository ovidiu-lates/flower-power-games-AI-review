from uuid import UUID

from sqlalchemy.orm import Session

from smart_review_ai.core.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from smart_review_ai.models.game import Game
from smart_review_ai.repositories.game_repository import GameRepository


class GameService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.games = GameRepository(session)

    def create_game(self, **values: object) -> Game:
        name = values["name"]
        if isinstance(name, str) and self.games.get_by_name(name) is not None:
            raise EntityAlreadyExistsError("Game name is already registered")
        game = self.games.create(**values)
        self.session.commit()
        return game

    def get_game(self, game_id: UUID) -> Game:
        game = self.games.get_by_id(game_id)
        if game is None:
            raise EntityNotFoundError("Game not found")
        return game

    def list_games(self) -> list[Game]:
        return self.games.list()

    def update_game(self, game_id: UUID, values: dict[str, object]) -> Game:
        game = self.get_game(game_id)
        name = values.get("name")
        if isinstance(name, str):
            existing = self.games.get_by_name(name)
            if existing is not None and existing.id != game_id:
                raise EntityAlreadyExistsError("Game name is already registered")
        game = self.games.update(game, values)
        self.session.commit()
        return game

    def delete_game(self, game_id: UUID) -> None:
        game = self.get_game(game_id)
        self.games.delete(game)
        self.session.commit()
