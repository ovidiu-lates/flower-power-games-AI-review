from fastapi import FastAPI

from smart_review_ai.api.routes import router

app = FastAPI(
    title="Smart Review AI",
    version="0.1.0",
)

app.include_router(router)
