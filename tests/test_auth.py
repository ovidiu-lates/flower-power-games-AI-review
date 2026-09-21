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


def test_oauth2_token_endpoint_accepts_form_data(client: TestClient) -> None:
    registration = client.post(
        "/auth/register",
        json={
            "username": "swaggeruser",
            "email": "swagger@example.com",
            "password": "correct horse battery staple",
        },
    )
    assert registration.status_code == 201

    response = client.post(
        "/auth/token",
        data={
            "username": "swaggeruser",
            "password": "correct horse battery staple",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_openapi_points_oauth2_authorize_to_token_endpoint(client: TestClient) -> None:
    openapi = client.get("/openapi.json").json()
    security_scheme = openapi["components"]["securitySchemes"]["OAuth2PasswordBearer"]

    assert security_scheme["type"] == "oauth2"
    assert security_scheme["flows"]["password"]["tokenUrl"] == "/auth/token"
