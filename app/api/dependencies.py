from typing import Annotated, cast

from fastapi import Depends, Request

from app.repositories.base import CatalogRepository
from app.services.catalog import CatalogService


def get_repository(request: Request) -> CatalogRepository:
    return cast(CatalogRepository, request.app.state.repository)


def get_catalog_service(
    repository: Annotated[CatalogRepository, Depends(get_repository)],
) -> CatalogService:
    return CatalogService(repository=repository)
