from typing import Any
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from smart_review_ai.models.game_insight import GameInsight
from smart_review_ai.models.game_insight_complaint import GameInsightComplaint
from smart_review_ai.models.game_insight_liked_aspect import GameInsightLikedAspect


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def game_payload(
    name: str = "Catan",
    *,
    min_players: int = 3,
    max_players: int = 4,
    min_play_time: int = 60,
    max_play_time: int = 120,
) -> dict[str, Any]:
    return {
        "name": name,
        "description": "A strategy game",
        "image_url": "https://example.com/catan.jpg",
        "min_players": min_players,
        "max_players": max_players,
        "min_play_time": min_play_time,
        "max_play_time": max_play_time,
    }


def create_game(client: TestClient, token: str) -> dict[str, Any]:
    response = client.post("/games", json=game_payload(), headers=auth_headers(token))
    assert response.status_code == 201
    return response.json()


def create_games(client: TestClient, token: str, names: list[str]) -> None:
    for name in names:
        response = client.post(
            "/games",
            json=game_payload(name),
            headers=auth_headers(token),
        )
        assert response.status_code == 201


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
    assert listed.json()["items"][0]["name"] == "Catan"
    assert listed.json()["page"] == 1
    assert listed.json()["page_size"] == 50
    assert listed.json()["total"] == 1
    assert listed.json()["total_pages"] == 1

    fetched = client.get(f"/games/{game_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Catan"

    assert client.patch(
        f"/games/{game_id}", json={"name": "Updated"}, headers=headers
    ).status_code == 405
    assert client.delete(f"/games/{game_id}", headers=headers).status_code == 405


def test_list_games_page_two_returns_second_page(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    create_games(client, token, ["Alpha", "Bravo", "Charlie"])

    response = client.get(
        "/games?page=2&page_size=2",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    body = response.json()
    assert [game["name"] for game in body["items"]] == ["Charlie"]
    assert body["page"] == 2
    assert body["page_size"] == 2
    assert body["total"] == 3
    assert body["total_pages"] == 2


def test_list_games_custom_page_size_and_empty_page(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    create_games(client, token, ["Alpha", "Bravo", "Charlie"])

    response = client.get(
        "/games?page=3&page_size=2",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 3
    assert body["total_pages"] == 2


def test_list_games_searches_full_partial_and_case_insensitive_name(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    create_games(client, token, ["The Settlers of Catan", "Catan Junior", "Azul"])
    headers = auth_headers(token)

    full_name = client.get("/games?search=The%20Settlers%20of%20Catan", headers=headers)
    assert [game["name"] for game in full_name.json()["items"]] == [
        "The Settlers of Catan"
    ]

    partial_name = client.get("/games?search=cata", headers=headers)
    assert [game["name"] for game in partial_name.json()["items"]] == [
        "Catan Junior",
        "The Settlers of Catan",
    ]

    case_insensitive = client.get("/games?search=AZUL", headers=headers)
    assert [game["name"] for game in case_insensitive.json()["items"]] == ["Azul"]


def test_empty_search_does_not_filter_results(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    create_games(client, token, ["Alpha", "Bravo"])
    headers = auth_headers(token)

    without_search = client.get("/games", headers=headers).json()
    with_empty_search = client.get("/games?search=%20%20", headers=headers).json()

    assert with_empty_search == without_search


def test_list_games_filters_supported_player_count(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)
    for name, minimum, maximum in [("Four Player", 2, 4), ("Two Player", 2, 2)]:
        response = client.post(
            "/games",
            json=game_payload(name, min_players=minimum, max_players=maximum),
            headers=headers,
        )
        assert response.status_code == 201

    response = client.get("/games?min_players=3", headers=headers)

    assert [game["name"] for game in response.json()["items"]] == ["Four Player"]


def test_list_games_combines_search_player_and_play_time_filters(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)
    games = [
        ("Catan Family", 3, 4, 60, 120),
        ("Catan Party", 3, 8, 20, 45),
        ("Azul Family", 2, 4, 30, 60),
    ]
    for name, minimum, maximum, shortest, longest in games:
        response = client.post(
            "/games",
            json=game_payload(
                name,
                min_players=minimum,
                max_players=maximum,
                min_play_time=shortest,
                max_play_time=longest,
            ),
            headers=headers,
        )
        assert response.status_code == 201

    response = client.get(
        "/games?search=catan&min_players=4&min_play_time=50&max_play_time=90",
        headers=headers,
    )
    body = response.json()

    assert [game["name"] for game in body["items"]] == ["Catan Family"]
    assert body["total"] == 1
    assert body["total_pages"] == 1


def test_omitting_filters_preserves_results_and_filtered_pagination_totals(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    headers = auth_headers(token)
    create_games(client, token, ["Alpha", "Bravo", "Charlie"])

    all_games = client.get("/games?page=1&page_size=2", headers=headers).json()
    filtered_games = client.get(
        "/games?search=a&page=2&page_size=1", headers=headers
    ).json()

    assert all_games["total"] == 3
    assert filtered_games["total"] == 3
    assert [game["name"] for game in filtered_games["items"]] == ["Bravo"]


def test_filter_with_no_matches_returns_empty_paginated_response(
    authenticated_client: tuple[TestClient, str],
) -> None:
    client, token = authenticated_client
    create_game(client, token)

    response = client.get(
        "/games?search=missing-game", headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 0
    assert response.json()["total_pages"] == 0


def test_list_games_supports_top_rated_sort(
    authenticated_client: tuple[TestClient, str],
    db_session: Session,
) -> None:
    client, token = authenticated_client
    first = create_game(client, token)
    second_response = client.post(
        "/games",
        json=game_payload("Azul"),
        headers=auth_headers(token),
    )
    assert second_response.status_code == 201

    db_session.add_all(
        [
            GameInsight(
                game_id=UUID(first["id"]),
                total_reviews=1,
                average_rating=7.0,
                positive_percentage=100,
                neutral_percentage=0,
                negative_percentage=0,
                easy_percentage=0,
                medium_percentage=100,
                hard_percentage=0,
            ),
            GameInsight(
                game_id=UUID(second_response.json()["id"]),
                total_reviews=1,
                average_rating=9.0,
                positive_percentage=100,
                neutral_percentage=0,
                negative_percentage=0,
                easy_percentage=0,
                medium_percentage=100,
                hard_percentage=0,
            ),
        ]
    )
    db_session.commit()

    response = client.get("/games?sort=top_rated", headers=auth_headers(token))

    assert [game["name"] for game in response.json()["items"]] == ["Azul", "Catan"]


def test_list_games_filters_by_latest_dominant_difficulty(
    authenticated_client: tuple[TestClient, str],
    db_session: Session,
) -> None:
    client, token = authenticated_client
    easy = create_game(client, token)
    hard_response = client.post(
        "/games",
        json=game_payload("Gloomhaven"),
        headers=auth_headers(token),
    )
    assert hard_response.status_code == 201
    db_session.add_all(
        [
            GameInsight(
                game_id=UUID(easy["id"]),
                total_reviews=1,
                average_rating=7.0,
                positive_percentage=100,
                neutral_percentage=0,
                negative_percentage=0,
                easy_percentage=80,
                medium_percentage=15,
                hard_percentage=5,
            ),
            GameInsight(
                game_id=UUID(hard_response.json()["id"]),
                total_reviews=1,
                average_rating=7.0,
                positive_percentage=100,
                neutral_percentage=0,
                negative_percentage=0,
                easy_percentage=5,
                medium_percentage=15,
                hard_percentage=80,
            ),
        ]
    )
    db_session.commit()

    response = client.get("/games?difficulty=hard", headers=auth_headers(token))

    assert [game["name"] for game in response.json()["items"]] == ["Gloomhaven"]


@pytest.mark.parametrize("query", ["page=0", "page=-1", "page_size=0", "page_size=-1", "page_size=101"])
def test_list_games_rejects_invalid_pagination(
    authenticated_client: tuple[TestClient, str],
    query: str,
) -> None:
    client, token = authenticated_client

    response = client.get(f"/games?{query}", headers=auth_headers(token))

    assert response.status_code == 422


@pytest.mark.parametrize(
    "query",
    ["min_players=0", "min_play_time=-1", "max_play_time=-1", "sort=unknown"],
)
def test_list_games_rejects_invalid_filters(
    authenticated_client: tuple[TestClient, str],
    query: str,
) -> None:
    client, token = authenticated_client

    response = client.get(f"/games?{query}", headers=auth_headers(token))

    assert response.status_code == 422


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
