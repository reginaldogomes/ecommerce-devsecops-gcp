import logging
from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response

from app.api.routes import router
from app.core.config import Settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import (
    configure_logging,
    extract_trace_id,
    request_id_ctx,
    trace_id_ctx,
)
from app.repositories.base import CatalogRepository
from app.repositories.memory import InMemoryCatalogRepository

logger = logging.getLogger("app.http")


def create_app(
    *,
    settings: Settings | None = None,
    repository: CatalogRepository | None = None,
) -> FastAPI:
    """Factory principal da aplicação FastAPI."""
    cfg = settings or Settings()
    configure_logging(cfg.log_level)

    application = FastAPI(title=cfg.app_name, version=cfg.app_version)
    application.state.settings = cfg
    application.state.repository = repository or InMemoryCatalogRepository()

    register_exception_handlers(application)
    application.include_router(router)

    @application.middleware("http")
    async def request_context_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        req_id = request.headers.get("X-Request-ID") or str(uuid4())
        trace_id = extract_trace_id(request.headers.get("X-Cloud-Trace-Context"))

        req_token = request_id_ctx.set(req_id)
        trace_token = trace_id_ctx.set(trace_id)
        start = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((perf_counter() - start) * 1000, 2)
            logger.exception(
                "http_request_failed method=%s path=%s duration_ms=%s",
                request.method,
                request.url.path,
                duration_ms,
            )
            raise
        else:
            duration_ms = round((perf_counter() - start) * 1000, 2)
            response.headers["X-Request-ID"] = req_id
            logger.info(
                "http_request method=%s path=%s status=%s duration_ms=%s",
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
            )
            return response
        finally:
            request_id_ctx.reset(req_token)
            trace_id_ctx.reset(trace_token)

    return application


app = create_app()
