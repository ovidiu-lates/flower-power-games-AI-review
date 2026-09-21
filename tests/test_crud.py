from typing import Any
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from smart_review_ai.models.game_insight import GameInsight
from smart_review_ai.models.game_insight_complaint import GameInsightComplaint
from smart_review_ai.models.game_insight_liked_aspect import GameInsightLikedAspect


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


def test_protected_domain_routes_require_authentication(client: TestClient) -> None:
    assert client.get("/games").status_code == 401
    assert client.post("/games", json=game_payload()).status_code == 401
    assert client.get(f"/games/{uuid4()}/reviews").status_code == 401
    assert client.get(f"/games/{uuid4()}/insight").status_code == 401


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
