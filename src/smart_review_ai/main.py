from fastapi import FastAPI

from smart_review_ai.api.router import router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Smart Review AI",
    version="0.1.0",
)

app.include_router(router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
