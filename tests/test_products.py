from fastapi.testclient import TestClient


def test_list_products(client: TestClient) -> None:
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert len(data["items"]) == 3
    assert "stock" in data["items"][0]


def test_get_product_success(client: TestClient) -> None:
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Notebook DevOps"


def test_get_product_not_found_problem_detail(client: TestClient) -> None:
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["title"] == "Resource Not Found"
    assert body["status"] == 404
    assert body["instance"] == "/products/999"
