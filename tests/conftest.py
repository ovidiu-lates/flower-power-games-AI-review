from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.db.database import Base
from smart_review_ai.main import app
from smart_review_ai.models import (  # noqa: F401
    Game,
    GameInsight,
    GameInsightComplaint,
    GameInsightLikedAspect,
    Review,
    ReviewAnalysis,
    ReviewComplaint,
    ReviewLikedAspect,
    User,
)

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture
def client() -> Generator[TestClient]:
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session]:
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def authenticated_client(client: TestClient) -> Generator[tuple[TestClient, str]]:
    response = client.post(
        "/auth/register",
        json={
            "username": "boardgamer",
            "email": "boardgamer@example.com",
            "password": "correct horse battery staple",
        },
    )
    assert response.status_code == 201
    login = client.post(
        "/auth/login",
        json={"username": "boardgamer", "password": "correct horse battery staple"},
    )
    assert login.status_code == 200
    yield client, login.json()["access_token"]
