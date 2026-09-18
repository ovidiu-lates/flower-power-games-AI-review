from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from smart_review_ai.api.dependencies.auth import get_current_active_user
from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.core.exceptions import EntityNotFoundError
from smart_review_ai.models.user import User
from smart_review_ai.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from smart_review_ai.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])
SessionDependency = Annotated[Session, Depends(get_db)]
AuthDependency = Annotated[User, Depends(get_current_active_user)]


def _not_found(error: EntityNotFoundError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    request: ReviewCreate,
    session: SessionDependency,
    current_user: AuthDependency,
) -> ReviewResponse:
    try:
        return ReviewService(session).create_review(
            user_id=current_user.id,
            **request.model_dump(),
        )
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.get("", response_model=list[ReviewResponse])
def list_reviews(session: SessionDependency, _: AuthDependency) -> list[ReviewResponse]:
    return ReviewService(session).list_reviews()


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
) -> ReviewResponse:
    try:
        return ReviewService(session).get_review(review_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: UUID,
    request: ReviewUpdate,
    session: SessionDependency,
    _: AuthDependency,
) -> ReviewResponse:
    try:
        return ReviewService(session).update_review(
            review_id, request.model_dump(exclude_unset=True)
        )
    except EntityNotFoundError as error:
        raise _not_found(error) from error


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: UUID,
    session: SessionDependency,
    _: AuthDependency,
) -> Response:
    try:
        ReviewService(session).delete_review(review_id)
    except EntityNotFoundError as error:
        raise _not_found(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
