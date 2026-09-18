from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from smart_review_ai.api.dependencies.auth import get_current_active_user
from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.core.exceptions import EntityNotFoundError
from smart_review_ai.models.user import User
from smart_review_ai.schemas.game_insight import (
    GameInsightCreate,
    GameInsightResponse,
    GameInsightUpdate,
)
from smart_review_ai.services.game_insights_service import GameInsightsService

router = APIRouter(prefix="/game-insights", tags=["game-insights"])
SessionDependency = Annotated[Session, Depends(get_db)]
AuthDependency = Annotated[User, Depends(get_current_active_user)]


def _not_found(error: EntityNotFoundError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("", response_model=GameInsightResponse, status_code=status.HTTP_201_CREATED)
def create_game_insights(
    request: GameInsightCreate,
    session: SessionDependency,
    _: AuthDependency,
) -> GameInsightResponse:
    values = request.model_dump(exclude_none=True)
    try:
        return GameInsightsService(session).create_game_insights(**values)
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.get("", response_model=list[GameInsightResponse])
def list_game_insights(
    session: SessionDependency,
    _: AuthDependency,
) -> list[GameInsightResponse]:
    return GameInsightsService(session).list_game_insights()


@router.get("/{insight_id}", response_model=GameInsightResponse)
def get_game_insights(
    insight_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
) -> GameInsightResponse:
    try:
        return GameInsightsService(session).get_game_insights(insight_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.patch("/{insight_id}", response_model=GameInsightResponse)
def update_game_insights(
    insight_id: UUID,
    request: GameInsightUpdate,
    session: SessionDependency,
    _: AuthDependency,
) -> GameInsightResponse:
    try:
        return GameInsightsService(session).update_game_insights(
            insight_id, request.model_dump(exclude_unset=True)
        )
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.delete("/{insight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game_insights(
    insight_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
) -> Response:
    try:
        GameInsightsService(session).delete_game_insights(insight_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
