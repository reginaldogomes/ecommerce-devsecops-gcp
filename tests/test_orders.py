from fastapi.testclient import TestClient


def test_create_order_decrements_stock(client: TestClient) -> None:
    before = client.get("/products/2").json()["stock"]

    response = client.post(
        "/orders",
        json={"product_id": 2, "quantity": 2},
        headers={"X-Request-ID": "req-123", "X-Cloud-Trace-Context": "trace-abc/1;o=1"},
    )
    assert response.status_code == 201
    assert response.headers["X-Request-ID"] == "req-123"
    body = response.json()
    assert body["product_id"] == 2
    assert body["quantity"] == 2
    assert body["total"] == 259.8
    assert body["status"] == "confirmed"
    assert body["order_id"]

    after = client.get("/products/2").json()["stock"]
    assert after == before - 2


def test_create_order_idempotency(client: TestClient) -> None:
    headers = {"Idempotency-Key": "idem-001"}
    first = client.post("/orders", json={"product_id": 2, "quantity": 3}, headers=headers)
    second = client.post("/orders", json={"product_id": 2, "quantity": 3}, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json() == second.json()
    assert client.get("/products/2").json()["stock"] == 47


def test_create_order_insufficient_stock(client: TestClient) -> None:
    response = client.post("/orders", json={"product_id": 1, "quantity": 50})
    assert response.status_code == 409
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["title"] == "Insufficient Stock"


def test_create_order_product_not_found(client: TestClient) -> None:
    response = client.post("/orders", json={"product_id": 999, "quantity": 1})
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"


def test_create_order_invalid_quantity(client: TestClient) -> None:
    response = client.post("/orders", json={"product_id": 1, "quantity": 0})
    assert response.status_code == 422
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["title"] == "Validation Error"
    assert len(body["errors"]) == 1
