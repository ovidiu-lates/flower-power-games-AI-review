from typing import Any
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from smart_review_ai.analysis.review_analyzer import ReviewAnalysisResult
from smart_review_ai.models.game import Game
from smart_review_ai.models.game_insight import GameInsight
from smart_review_ai.models.game_insight_complaint import GameInsightComplaint
from smart_review_ai.models.game_insight_liked_aspect import GameInsightLikedAspect
from smart_review_ai.models.review import Review
from smart_review_ai.models.user import User
from smart_review_ai.services.game_insights_service import GameInsightsService
from smart_review_ai.services.review_service import ReviewService


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def game_payload(name: str = "Catan") -> dict[str, Any]:
    return {
        "name": name,
        "description": "A strategy game",
        "image_url": "https://example.com/catan.jpg",
        "min_players": 3,
        "max_players": 4,
        "min_play_time": 60,
        "max_play_time": 120,
    }


def create_game(client: TestClient, token: str) -> dict[str, Any]:
    response = client.post("/games", json=game_payload(), headers=auth_headers(token))
    assert response.status_code == 201
    return response.json()


class FakeReviewAnalyzer:
    def __init__(self, *results: ReviewAnalysisResult) -> None:
        self.results = list(results)

    def analyze(self, *, content: str, rating: int) -> ReviewAnalysisResult:
        assert content
        assert rating
        return self.results.pop(0)


class FakeGameInsightExplainer:
    def __init__(self, explanation: str = "Players mostly like this game.") -> None:
        self.explanation = explanation
        self.review_count = 0

    def explain(
        self, *, game_name: str, insight: GameInsight, reviews: list[Review]
    ) -> str:
        assert game_name
        assert insight.total_reviews
        self.review_count = len(reviews)
        return self.explanation


def test_protected_domain_routes_require_authentication(client: TestClient) -> None:
    assert client.get("/games").status_code == 401
    assert client.post("/games", json=game_payload()).status_code == 401
    assert client.get(f"/games/{uuid4()}/reviews").status_code == 401
    assert client.get(f"/games/{uuid4()}/insight").status_code == 401
    assert client.get(f"/games/{uuid4()}/insight/explanation").status_code == 401


def test_game_read_and_create_only(authenticated_client: tuple[TestClient, str]) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)

    created = client.post("/games", json=game_payload(), headers=headers)
    assert created.status_code == 201
    game_id = created.json()["id"]

    listed = client.get("/games", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/games/{game_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Catan"

    assert client.patch(
        f"/games/{game_id}", json={"name": "Updated"}, headers=headers
    ).status_code == 405
    assert client.delete(f"/games/{game_id}", headers=headers).status_code == 405


def test_game_scoped_review_creation_and_listing(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)
    game = create_game(client, token)

    created = client.post(
        f"/games/{game['id']}/reviews",
        json={"rating": 8, "content": "Great game"},
        headers=headers,
    )
    assert created.status_code == 201
    review = created.json()
    assert review["game_id"] == game["id"]
    assert review["user_id"]

    listed = client.get(f"/games/{game['id']}/reviews", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["id"] == review["id"]

    fetched = client.get(f"/reviews/{review['id']}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["content"] == "Great game"

    assert client.post(
        "/reviews",
        json={"rating": 8, "content": "Legacy endpoint"},
        headers=headers,
    ).status_code == 404
    assert client.get("/reviews", headers=headers).status_code == 404
    assert client.patch(
        f"/reviews/{review['id']}", json={"rating": 9}, headers=headers
    ).status_code == 405
    assert client.delete(f"/reviews/{review['id']}", headers=headers).status_code == 405


def test_review_creation_analyzes_review_and_updates_game_insight(
    db_session: Session,
) -> None:
    user = User(
        username="reviewer",
        email="reviewer@example.com",
        password_hash="not-used",
    )
    game = Game(**game_payload("Terraforming Mars"))
    db_session.add_all([user, game])
    db_session.commit()

    analyzer = FakeReviewAnalyzer(
        ReviewAnalysisResult(
            sentiment="positive",
            confidence=0.94,
            perceived_difficulty="hard",
            liked_aspects=["strategy", "components"],
            complaints=["slow setup"],
        )
    )

    review = ReviewService(db_session, analyzer=analyzer).create_review(
        user_id=user.id,
        game_id=game.id,
        rating=9,
        content="Great strategy and components, but setup is slow",
    )
    insight = GameInsightsService(db_session).get_game_insight(game.id)

    assert review.analysis is not None
    assert review.analysis.sentiment == "positive"
    assert review.analysis.perceived_difficulty == "hard"
    assert [aspect.aspect for aspect in review.analysis.liked_aspects] == [
        "strategy",
        "components",
    ]
    assert [complaint.complaint for complaint in review.analysis.complaints] == [
        "slow setup"
    ]
    assert insight.total_reviews == 1
    assert insight.average_rating == 9
    assert insight.positive_percentage == 100
    assert insight.hard_percentage == 100
    assert [(item.aspect, item.occurrence_count) for item in insight.liked_aspects] == [
        ("strategy", 1),
        ("components", 1),
    ]
    assert [(item.complaint, item.occurrence_count) for item in insight.complaints] == [
        ("slow setup", 1)
    ]


def test_review_creation_updates_existing_game_insight(
    db_session: Session,
) -> None:
    user = User(
        username="insight-reviewer",
        email="insight-reviewer@example.com",
        password_hash="not-used",
    )
    game = Game(**game_payload("Ark Nova"))
    db_session.add_all([user, game])
    db_session.commit()

    analyzer = FakeReviewAnalyzer(
        ReviewAnalysisResult(
            sentiment="positive",
            confidence=0.9,
            perceived_difficulty="hard",
            liked_aspects=["replayability"],
            complaints=[],
        ),
        ReviewAnalysisResult(
            sentiment="neutral",
            confidence=0.8,
            perceived_difficulty="medium",
            liked_aspects=["replayability"],
            complaints=["downtime"],
        ),
    )

    ReviewService(db_session, analyzer=analyzer).create_review(
        user_id=user.id,
        game_id=game.id,
        rating=9,
        content="Great replay value",
    )
    first_insight = GameInsightsService(db_session).get_game_insight(game.id)

    ReviewService(db_session, analyzer=analyzer).create_review(
        user_id=user.id,
        game_id=game.id,
        rating=5,
        content="Still replayable, but has downtime",
    )
    updated_insight = GameInsightsService(db_session).get_game_insight(game.id)
    all_insights = list(db_session.scalars(select(GameInsight)))

    assert updated_insight.id == first_insight.id
    assert len(all_insights) == 1
    assert updated_insight.total_reviews == 2
    assert updated_insight.average_rating == 7
    assert updated_insight.positive_percentage == 50
    assert updated_insight.neutral_percentage == 50
    assert updated_insight.hard_percentage == 50
    assert updated_insight.medium_percentage == 50
    assert [(item.aspect, item.occurrence_count) for item in updated_insight.liked_aspects] == [
        ("replayability", 2)
    ]
    assert [(item.complaint, item.occurrence_count) for item in updated_insight.complaints] == [
        ("downtime", 1)
    ]


def test_game_insight_explanation_uses_requested_review_limit(
    db_session: Session,
) -> None:
    user = User(
        username="explanation-reviewer",
        email="explanation-reviewer@example.com",
        password_hash="not-used",
    )
    game = Game(**game_payload("Wingspan"))
    db_session.add_all([user, game])
    db_session.commit()

    analyzer = FakeReviewAnalyzer(
        ReviewAnalysisResult(
            sentiment="positive",
            confidence=0.9,
            perceived_difficulty="medium",
            liked_aspects=["theme"],
            complaints=[],
        ),
        ReviewAnalysisResult(
            sentiment="positive",
            confidence=0.85,
            perceived_difficulty="medium",
            liked_aspects=["components"],
            complaints=[],
        ),
    )
    review_service = ReviewService(db_session, analyzer=analyzer)
    review_service.create_review(
        user_id=user.id,
        game_id=game.id,
        rating=8,
        content="Beautiful theme",
    )
    review_service.create_review(
        user_id=user.id,
        game_id=game.id,
        rating=9,
        content="Great components",
    )

    explainer = FakeGameInsightExplainer("Players praise the theme and components.")
    explanation, review_count = GameInsightsService(
        db_session, explainer=explainer
    ).explain_game_insight(game.id, review_limit=1)

    assert explanation == "Players praise the theme and components."
    assert review_count == 1
    assert explainer.review_count == 1


def test_game_scoped_review_rejects_unknown_game(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client

    response = client.post(
        f"/games/{uuid4()}/reviews",
        json={"rating": 8, "content": "Unknown game"},
        headers=auth_headers(token),
    )
    assert response.status_code == 404


def test_game_insight_retrieval_includes_nested_children(
    authenticated_client: tuple[TestClient, str],
    db_session: Session,
) -> None:
    client, token = authenticated_client
    game = create_game(client, token)

    insight = GameInsight(
        game_id=UUID(game["id"]),
        total_reviews=100,
        average_rating=8.2,
        positive_percentage=70,
        neutral_percentage=20,
        negative_percentage=10,
        easy_percentage=15,
        medium_percentage=60,
        hard_percentage=25,
    )
    insight.liked_aspects.append(
        GameInsightLikedAspect(
            aspect="strategy", occurrence_count=40, percentage=40.0
        )
    )
    insight.complaints.append(
        GameInsightComplaint(
            complaint="long setup", occurrence_count=15, percentage=15.0
        )
    )
    db_session.add(insight)
    db_session.commit()

    response = client.get(
        f"/games/{game['id']}/insight",
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["game_id"] == game["id"]
    assert body["liked_aspects"] == [
        {"aspect": "strategy", "occurrence_count": 40, "percentage": 40.0}
    ]
    assert body["complaints"] == [
        {"complaint": "long setup", "occurrence_count": 15, "percentage": 15.0}
    ]


def test_missing_game_insight_and_old_insight_crud_are_unavailable(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)

    assert client.get(f"/games/{uuid4()}/insight", headers=headers).status_code == 404
    assert client.get("/game-insights", headers=headers).status_code == 404
    assert client.post("/game-insights", headers=headers).status_code == 404
