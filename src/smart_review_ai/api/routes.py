from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
reviews: dict[int, "ReviewResponse"] = {}


class ReviewRequest(BaseModel):
    game_id: int
    comment: str


class ReviewResponse(ReviewRequest):
    id: int


@router.post("/reviews", response_model=ReviewResponse, status_code=201)
def create_review(review: ReviewRequest):
    review_id = len(reviews) + 1
    saved_review = ReviewResponse(id=review_id, **review.model_dump())
    reviews[review_id] = saved_review
    return saved_review


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int):
    review = reviews.get(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review