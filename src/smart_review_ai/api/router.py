from fastapi import APIRouter

from smart_review_ai.api import auth, games, reviews

router = APIRouter()
router.include_router(auth.router)
router.include_router(games.router)
router.include_router(reviews.router)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
