from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_login_preflight_returns_cors_headers():
    response = client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "POST" in response.headers["access-control-allow-methods"]


def test_login_endpoint_returns_success_response():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["token"]
