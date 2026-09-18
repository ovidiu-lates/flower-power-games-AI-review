from fastapi.testclient import TestClient

from smart_review_ai.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_review_analysis_includes_complaints():
    response = client.post(
        "/reviews/analyze",
        json={"comment": "The rules are confusing and setup takes forever."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "complaints": ["confusing rules", "long setup"],
    }
