from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from smart_review_ai.api.dependencies.auth import get_current_active_user
from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.core.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    ReviewAnalysisUnavailableError,
    ServiceUnavailableError,
)
from smart_review_ai.models.user import User
from smart_review_ai.schemas.game import GameCreate, GameResponse, PaginatedGameResponse
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


@router.get("", response_model=PaginatedGameResponse)
def list_games(
    session: SessionDependency,
    _: AuthDependency,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    search: str | None = Query(default=None, max_length=255),
    min_players: int | None = Query(default=None, ge=1),
    min_play_time: int | None = Query(default=None, ge=0),
    max_play_time: int | None = Query(default=None, ge=0),
    difficulty: Literal["easy", "medium", "hard"] | None = Query(default=None),
    sort: Literal["top_rated"] | None = Query(default=None),
) -> PaginatedGameResponse:
    games, total = GameService(session).list_games_paginated(
        page,
        page_size,
        search=search,
        min_players=min_players,
        min_play_time=min_play_time,
        max_play_time=max_play_time,
        difficulty=difficulty,
        sort=sort,
    )
    total_pages = (total + page_size - 1) // page_size
    return PaginatedGameResponse(
        items=games,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


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
    except ReviewAnalysisUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


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


@router.post(
    "/{game_id}/insight/explanation",
    response_model=GameInsightExplanationResponse,
)
def explain_game_insight(
    game_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
    review_count: int = Query(default=5, ge=1, le=20),
) -> GameInsightExplanationResponse:
    try:
        explanation, analyzed_review_count = GameInsightsService(session).explain_game_insight(
            game_id,
            review_count,
        )
        return GameInsightExplanationResponse(
            game_id=game_id,
            review_count=analyzed_review_count,
            explanation=explanation,
        )
    except EntityNotFoundError as error:
        raise _not_found(error) from error
    except ServiceUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
