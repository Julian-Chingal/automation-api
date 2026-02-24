import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(
            f"[{exc.error_code}] {exc.message} | Details: {exc.details}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception occurred")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error_code": "INTERNAL_001",
                "message": "An unexpected internal error occurred.",
                "details": {},
            },
        )