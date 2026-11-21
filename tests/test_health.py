from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.memory import InMemoryCatalogRepository


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_liveness(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_ok(client: TestClient) -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "checks": {"repository": "ok"}}


def test_readiness_unavailable() -> None:
    unhealthy_app = create_app(repository=InMemoryCatalogRepository(healthy=False))
    unhealthy_client = TestClient(unhealthy_app)

    response = unhealthy_client.get("/health/ready")
    assert response.status_code == 503
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["title"] == "Service Unavailable"
    assert body["status"] == 503
