from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from smart_review_ai.api.dependencies.auth import get_current_active_user
from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.core.exceptions import EntityNotFoundError
from smart_review_ai.models.user import User
from smart_review_ai.schemas.review import ReviewResponse, UserReviewResponse
from smart_review_ai.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])
SessionDependency = Annotated[Session, Depends(get_db)]
AuthDependency = Annotated[User, Depends(get_current_active_user)]


def _not_found(error: EntityNotFoundError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/mine", response_model=list[UserReviewResponse])
def list_my_reviews(
    session: SessionDependency,
    current_user: AuthDependency,
) -> list[UserReviewResponse]:
    reviews = ReviewService(session).list_reviews_for_user(current_user.id)
    return [
        UserReviewResponse(
            id=review.id,
            user_id=review.user_id,
            game_id=review.game_id,
            rating=review.rating,
            content=review.content,
            created_at=review.created_at,
            updated_at=review.updated_at,
            game_name=review.game.name,
            game_image_url=review.game.image_url,
        )
        for review in reviews
    ]


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
