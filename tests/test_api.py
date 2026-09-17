from fastapi.testclient import TestClient

from smart_review_ai.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_review():
    response = client.post(
        "/api/reviews",
        json={"game_id": 1, "comment": "A great strategy game."},
    )

    assert response.status_code == 201
    review = response.json()
    assert review["game_id"] == 1
    assert review["comment"] == "A great strategy game."

    response = client.get(f"/api/reviews/{review['id']}")

    assert response.status_code == 200
    assert response.json() == review
