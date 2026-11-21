from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from app.api.dependencies import get_catalog_service
from app.schemas.catalog import (
    HealthOut,
    OrderCreate,
    OrderOut,
    ProductListOut,
    ProductOut,
    ReadinessOut,
)
from app.services.catalog import CatalogService

router = APIRouter()

CatalogServiceDep = Annotated[CatalogService, Depends(get_catalog_service)]


@router.get("/health", response_model=HealthOut, tags=["Observability"])
def health() -> HealthOut:
    return HealthOut(status="ok")


@router.get("/health/live", response_model=HealthOut, tags=["Observability"])
def liveness() -> HealthOut:
    return HealthOut(status="alive")


@router.get("/health/ready", response_model=ReadinessOut, tags=["Observability"])
def readiness(service: CatalogServiceDep) -> ReadinessOut:
    return service.check_readiness()


@router.get("/products", response_model=ProductListOut, tags=["Catalog"])
def list_products(service: CatalogServiceDep) -> ProductListOut:
    return service.list_products()


@router.get("/products/{product_id}", response_model=ProductOut, tags=["Catalog"])
def get_product(product_id: int, service: CatalogServiceDep) -> ProductOut:
    return service.get_product(product_id)


@router.post(
    "/orders",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Orders"],
)
def create_order(
    payload: OrderCreate,
    service: CatalogServiceDep,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> OrderOut:
    return service.create_order(payload, idempotency_key=idempotency_key)
