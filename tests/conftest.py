import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.memory import InMemoryCatalogRepository


@pytest.fixture
def repository() -> InMemoryCatalogRepository:
    return InMemoryCatalogRepository()


@pytest.fixture
def client(repository: InMemoryCatalogRepository) -> TestClient:
    app = create_app(repository=repository)
    return TestClient(app)
