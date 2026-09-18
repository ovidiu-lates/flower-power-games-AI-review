from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from smart_review_ai.api.dependencies.auth import get_current_active_user
from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.core.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from smart_review_ai.models.user import User
from smart_review_ai.schemas.game import GameCreate, GameResponse, GameUpdate
from smart_review_ai.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])
SessionDependency = Annotated[Session, Depends(get_db)]
AuthDependency = Annotated[User, Depends(get_current_active_user)]


def _not_found(error: EntityNotFoundError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(request: GameCreate, session: SessionDependency, _: AuthDependency) -> GameResponse:
    try:
        return GameService(session).create_game(**request.model_dump())
    except EntityAlreadyExistsError as error:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.get("", response_model=list[GameResponse])
def list_games(session: SessionDependency, _: AuthDependency) -> list[GameResponse]:
    return GameService(session).list_games()


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: UUID, session: SessionDependency, _: AuthDependency) -> GameResponse:
    try:
        return GameService(session).get_game(game_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.patch("/{game_id}", response_model=GameResponse)
def update_game(
    game_id: UUID,
    request: GameUpdate,
    session: SessionDependency,
    _: AuthDependency,
) -> GameResponse:
    try:
        return GameService(session).update_game(
            game_id, request.model_dump(exclude_unset=True)
        )
    except EntityNotFoundError as error:
        raise _not_found(error) from error
    except EntityAlreadyExistsError as error:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: UUID, session: SessionDependency, _: AuthDependency) -> Response:
    try:
        GameService(session).delete_game(game_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
