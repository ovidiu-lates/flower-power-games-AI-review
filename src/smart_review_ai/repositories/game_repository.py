from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from smart_review_ai.models.game import Game


class GameRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, game_id: UUID) -> Game | None:
        return self.session.get(Game, game_id)

    def list(self) -> list[Game]:
        return list(self.session.scalars(select(Game).order_by(Game.name)))

    def get_by_name(self, name: str) -> Game | None:
        statement = select(Game).where(Game.name == name)
        return self.session.scalar(statement)

    def create(self, **values: object) -> Game:
        game = Game(**values)
        self.session.add(game)
        self.session.flush()
        self.session.refresh(game)
        return game

    def update(self, game: Game, values: dict[str, object]) -> Game:
        for field, value in values.items():
            setattr(game, field, value)
        self.session.flush()
        self.session.refresh(game)
        return game

    def delete(self, game: Game) -> None:
        self.session.delete(game)
        self.session.flush()
