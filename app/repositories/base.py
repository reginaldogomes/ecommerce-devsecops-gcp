from typing import Protocol

from app.schemas.catalog import OrderOut, ProductOut


class CatalogRepository(Protocol):
    """Contrato de persistência para catálogo e pedidos."""

    def is_healthy(self) -> bool: ...

    def list_products(self) -> list[ProductOut]: ...

    def get_product(self, product_id: int) -> ProductOut | None: ...

    def create_order_atomic(
        self,
        *,
        product_id: int,
        quantity: int,
        order_id: str,
        idempotency_key: str | None = None,
    ) -> OrderOut: ...
