from fastapi.testclient import TestClient


def test_register_login_by_username_and_me(client: TestClient) -> None:
    registration = client.post(
        "/auth/register",
        json={
            "username": "boardgamer",
            "email": "boardgamer@example.com",
            "password": "correct horse battery staple",
        },
    )
    assert registration.status_code == 201
    assert "password_hash" not in registration.json()

    login = client.post(
        "/auth/login",
        json={"username": "boardgamer", "password": "correct horse battery staple"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "boardgamer"


def test_login_does_not_use_email(client: TestClient) -> None:
    client.post(
        "/auth/register",
        json={
            "username": "boardgamer",
            "email": "boardgamer@example.com",
            "password": "correct horse battery staple",
        },
    )

    response = client.post(
        "/auth/login",
        json={"username": "boardgamer@example.com", "password": "correct horse battery staple"},
    )
    assert response.status_code == 401
