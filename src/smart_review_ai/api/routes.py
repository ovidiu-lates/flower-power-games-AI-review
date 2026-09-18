from fastapi import APIRouter
from pydantic import BaseModel

from smart_review_ai.services.review_service import analyze_review

router = APIRouter()


class ReviewAnalysisRequest(BaseModel):
    comment: str


class ReviewAnalysisResponse(BaseModel):
    complaints: list[str]


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/reviews/analyze", response_model=ReviewAnalysisResponse)
def analyze_review_endpoint(request: ReviewAnalysisRequest):
    return analyze_review(request.comment)
