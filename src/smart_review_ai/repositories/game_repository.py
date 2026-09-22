from __future__ import annotations

from typing import Literal
from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from smart_review_ai.models.game import Game
from smart_review_ai.models.game_insight import GameInsight


class GameRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, game_id: UUID) -> Game | None:
        return self.session.get(Game, game_id)

    def list(self) -> list[Game]:
        return list(self.session.scalars(select(Game).order_by(Game.name)))

    def list_paginated(
        self,
        page: int,
        page_size: int,
        *,
        search: str | None = None,
        min_players: int | None = None,
        min_play_time: int | None = None,
        max_play_time: int | None = None,
        difficulty: Literal["easy", "medium", "hard"] | None = None,
        sort: Literal["top_rated"] | None = None,
    ) -> tuple[list[Game], int]:
        statement = self._filtered_statement(
            search=search,
            min_players=min_players,
            min_play_time=min_play_time,
            max_play_time=max_play_time,
            difficulty=difficulty,
        )
        total = self.session.scalar(
            select(func.count()).select_from(statement.subquery())
        ) or 0
        offset = (page - 1) * page_size
        if sort == "top_rated":
            latest_rating = (
                select(GameInsight.average_rating)
                .where(GameInsight.game_id == Game.id)
                .order_by(GameInsight.generated_at.desc())
                .limit(1)
                .scalar_subquery()
            )
            statement = statement.order_by(
                case((latest_rating.is_(None), 1), else_=0),
                latest_rating.desc(),
                Game.name,
                Game.id,
            )
        else:
            statement = statement.order_by(Game.name, Game.id)
        statement = statement.offset(offset).limit(page_size)
        return list(self.session.scalars(statement)), total

    def _filtered_statement(
        self,
        *,
        search: str | None,
        min_players: int | None,
        min_play_time: int | None,
        max_play_time: int | None,
        difficulty: Literal["easy", "medium", "hard"] | None,
    ):
        statement = select(Game)
        if search and search.strip():
            statement = statement.where(Game.name.ilike(f"%{search.strip()}%"))
        if min_players is not None:
            statement = statement.where(
                Game.min_players <= min_players,
                Game.max_players >= min_players,
            )
        if min_play_time is not None:
            statement = statement.where(Game.max_play_time >= min_play_time)
        if max_play_time is not None:
            statement = statement.where(Game.min_play_time <= max_play_time)
        if difficulty is not None:
            difficulty_percentages = {
                "easy": GameInsight.easy_percentage,
                "medium": GameInsight.medium_percentage,
                "hard": GameInsight.hard_percentage,
            }
            selected_percentage = (
                select(difficulty_percentages[difficulty])
                .where(GameInsight.game_id == Game.id)
                .order_by(GameInsight.generated_at.desc())
                .limit(1)
                .scalar_subquery()
            )
            other_percentages = [
                percentage
                for name, percentage in difficulty_percentages.items()
                if name != difficulty
            ]
            statement = statement.where(
                selected_percentage >= (
                    select(other_percentages[0])
                    .where(GameInsight.game_id == Game.id)
                    .order_by(GameInsight.generated_at.desc())
                    .limit(1)
                    .scalar_subquery()
                ),
                selected_percentage >= (
                    select(other_percentages[1])
                    .where(GameInsight.game_id == Game.id)
                    .order_by(GameInsight.generated_at.desc())
                    .limit(1)
                    .scalar_subquery()
                ),
            )
        return statement

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
