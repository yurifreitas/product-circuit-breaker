import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

logger = structlog.get_logger()

def setup_logging(app):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()

        logger.info(
            "request_start",
            method=request.method,
            path=request.url.path,
            client=str(request.client),
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.exception("request_exception", error=str(exc))
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

        duration = time.time() - start_time
        logger.info(
            "request_end",
            status_code=response.status_code,
            duration=f"{duration:.4f}s",
        )
        return response
