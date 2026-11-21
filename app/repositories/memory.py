from dataclasses import dataclass
from threading import Lock

from app.core.exceptions import InsufficientStockError, NotFoundError
from app.schemas.catalog import OrderOut, ProductOut


@dataclass
class _ProductRecord:
    id: int
    name: str
    price: float
    stock: int

    def to_schema(self) -> ProductOut:
        return ProductOut(
            id=self.id,
            name=self.name,
            price=self.price,
            stock=self.stock,
        )


class InMemoryCatalogRepository:
    """Repositório thread-safe em memória para desenvolvimento e testes."""

    def __init__(self, *, healthy: bool = True) -> None:
        self._healthy = healthy
        self._lock = Lock()
        self._products: dict[int, _ProductRecord] = {
            1: _ProductRecord(id=1, name="Notebook DevOps", price=3499.90, stock=15),
            2: _ProductRecord(id=2, name="Mouse Wireless", price=129.90, stock=50),
            3: _ProductRecord(id=3, name="Teclado Mecanico", price=399.90, stock=30),
        }
        self._orders_by_idempotency: dict[str, OrderOut] = {}

    def is_healthy(self) -> bool:
        return self._healthy

    def list_products(self) -> list[ProductOut]:
        with self._lock:
            return [record.to_schema() for record in self._products.values()]

    def get_product(self, product_id: int) -> ProductOut | None:
        with self._lock:
            record = self._products.get(product_id)
            return record.to_schema() if record is not None else None

    def create_order_atomic(
        self,
        *,
        product_id: int,
        quantity: int,
        order_id: str,
        idempotency_key: str | None = None,
    ) -> OrderOut:
        with self._lock:
            if idempotency_key and idempotency_key in self._orders_by_idempotency:
                return self._orders_by_idempotency[idempotency_key]

            record = self._products.get(product_id)
            if record is None:
                raise NotFoundError(f"Produto {product_id} nao encontrado.")

            if record.stock < quantity:
                raise InsufficientStockError(
                    f"Estoque insuficiente para o produto {product_id}: "
                    f"disponivel={record.stock}, solicitado={quantity}."
                )

            record.stock -= quantity
            order = OrderOut(
                order_id=order_id,
                product_id=record.id,
                quantity=quantity,
                unit_price=record.price,
                total=round(record.price * quantity, 2),
                status="confirmed",
            )
            if idempotency_key:
                self._orders_by_idempotency[idempotency_key] = order
            return order
