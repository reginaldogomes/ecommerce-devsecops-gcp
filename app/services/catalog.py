from uuid import uuid4

from app.core.exceptions import NotFoundError, ServiceUnavailableError
from app.repositories.base import CatalogRepository
from app.schemas.catalog import OrderCreate, OrderOut, ProductListOut, ProductOut, ReadinessOut


class CatalogService:
    """Camada de regras de negócio do catálogo e pedidos."""

    def __init__(self, repository: CatalogRepository) -> None:
        self._repository = repository

    def check_readiness(self) -> ReadinessOut:
        if not self._repository.is_healthy():
            raise ServiceUnavailableError("Catalog repository is unavailable.")
        return ReadinessOut(status="ready", checks={"repository": "ok"})

    def list_products(self) -> ProductListOut:
        items = self._repository.list_products()
        return ProductListOut(items=items, count=len(items))

    def get_product(self, product_id: int) -> ProductOut:
        item = self._repository.get_product(product_id)
        if item is None:
            raise NotFoundError(f"Produto {product_id} nao encontrado.")
        return item

    def create_order(
        self,
        payload: OrderCreate,
        *,
        idempotency_key: str | None = None,
    ) -> OrderOut:
        order_id = str(uuid4())
        return self._repository.create_order_atomic(
            product_id=payload.product_id,
            quantity=payload.quantity,
            order_id=order_id,
            idempotency_key=idempotency_key,
        )
