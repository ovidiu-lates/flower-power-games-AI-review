from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from smart_review_ai.api.dependencies.auth import get_current_active_user
from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.core.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    ServiceUnavailableError,
)
from smart_review_ai.models.user import User
from smart_review_ai.schemas.game import GameCreate, GameResponse
from smart_review_ai.schemas.game_insight import (
    GameInsightExplanationResponse,
    GameInsightResponse,
)
from smart_review_ai.schemas.review import ReviewCreate, ReviewResponse
from smart_review_ai.services.game_insights_service import GameInsightsService
from smart_review_ai.services.game_service import GameService
from smart_review_ai.services.review_service import ReviewService

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


@router.get("/{game_id}/reviews", response_model=list[ReviewResponse])
def list_game_reviews(
    game_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
) -> list[ReviewResponse]:
    try:
        return ReviewService(session).list_reviews_for_game(game_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.post(
    "/{game_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_game_review(
    game_id: UUID,
    request: ReviewCreate,
    session: SessionDependency,
    current_user: AuthDependency,
) -> ReviewResponse:
    try:
        return ReviewService(session).create_review(
            user_id=current_user.id,
            game_id=game_id,
            **request.model_dump(),
        )
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.get("/{game_id}/insight", response_model=GameInsightResponse)
def get_game_insight(
    game_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
) -> GameInsightResponse:
    try:
        return GameInsightsService(session).get_game_insight(game_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.get(
    "/{game_id}/insight/explanation",
    response_model=GameInsightExplanationResponse,
)
def explain_game_insight(
    game_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
    review_limit: int = Query(default=5, ge=1, le=20),
) -> GameInsightExplanationResponse:
    try:
        explanation, review_count = GameInsightsService(session).explain_game_insight(
            game_id=game_id,
            review_limit=review_limit,
        )
        return GameInsightExplanationResponse(
            game_id=game_id,
            review_count=review_count,
            explanation=explanation,
        )
    except EntityNotFoundError as error:
        raise _not_found(error) from error
    except ServiceUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
