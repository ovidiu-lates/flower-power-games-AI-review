from typing import Any
from uuid import uuid4

from fastapi.testclient import TestClient


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


def review_payload(game_id: str) -> dict[str, Any]:
    return {"game_id": game_id, "rating": 8, "content": "Great game"}


def insight_payload(game_id: str) -> dict[str, Any]:
    return {
        "game_id": game_id,
        "total_reviews": 10,
        "average_rating": 8.2,
        "positive_percentage": 70,
        "neutral_percentage": 20,
        "negative_percentage": 10,
        "easy_percentage": 20,
        "medium_percentage": 50,
        "hard_percentage": 30,
    }


def create_game(client: TestClient, token: str) -> dict[str, Any]:
    response = client.post("/games", json=game_payload(), headers=auth_headers(token))
    assert response.status_code == 201
    return response.json()


def test_protected_crud_requires_authentication(client: TestClient) -> None:
    response = client.get("/reviews")
    assert response.status_code == 401


def test_review_crud(authenticated_client: tuple[TestClient, str]) -> None:
    client, token = authenticated_client
    game = create_game(client, token)
    headers = auth_headers(token)

    created = client.post("/reviews", json=review_payload(game["id"]), headers=headers)
    assert created.status_code == 201
    review_id = created.json()["id"]
    assert created.json()["user_id"]

    listed = client.get("/reviews", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/reviews/{review_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["content"] == "Great game"

    updated = client.patch(
        f"/reviews/{review_id}",
        json={"rating": 9},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["rating"] == 9

    deleted = client.delete(f"/reviews/{review_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/reviews/{review_id}", headers=headers).status_code == 404

    missing_id = str(uuid4())
    assert client.get(f"/reviews/{missing_id}", headers=headers).status_code == 404
    assert client.patch(
        f"/reviews/{missing_id}", json={"rating": 5}, headers=headers
    ).status_code == 404
    assert client.delete(f"/reviews/{missing_id}", headers=headers).status_code == 404


def test_game_crud(authenticated_client: tuple[TestClient, str]) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)

    created = client.post("/games", json=game_payload(), headers=headers)
    assert created.status_code == 201
    game_id = created.json()["id"]

    listed = client.get("/games", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.patch(
        f"/games/{game_id}", json={"name": "Catan Updated"}, headers=headers
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Catan Updated"

    deleted = client.delete(f"/games/{game_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/games/{game_id}", headers=headers).status_code == 404


def test_game_insight_crud(authenticated_client: tuple[TestClient, str]) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)
    game = create_game(client, token)

    created = client.post(
        "/game-insights", json=insight_payload(game["id"]), headers=headers
    )
    assert created.status_code == 201
    insight_id = created.json()["id"]

    listed = client.get("/game-insights", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/game-insights/{insight_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["total_reviews"] == 10

    updated = client.patch(
        f"/game-insights/{insight_id}",
        json={"average_rating": 8.5},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["average_rating"] == 8.5

    deleted = client.delete(f"/game-insights/{insight_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/game-insights/{insight_id}", headers=headers).status_code == 404

    missing_id = str(uuid4())
    assert client.get(f"/game-insights/{missing_id}", headers=headers).status_code == 404
    assert client.patch(
        f"/game-insights/{missing_id}",
        json={"total_reviews": 1},
        headers=headers,
    ).status_code == 404
    assert client.delete(f"/game-insights/{missing_id}", headers=headers).status_code == 404
