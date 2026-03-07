from contextlib import asynccontextmanager
import logging
import sys

from core.handlers import register_exception_handlers
from core.logger import configure_logging
from core.security import api_key_auth
from core.database import db_manager
from core.settings import settings
from api.v1.api import api_router

from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI

# Logging
configure_logging()
logger = logging.getLogger(__name__)

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting application in environment: {settings.APP_ENV}")

    if not settings.DATABASES:
        logger.critical("No databases configured")
        sys.exit(1)
    
    app.state.db_manager = db_manager

    logger.info("Application ready.")
    yield

    logger.info("Shutting down database connections...")
    db_manager.dispose_all()
    logger.info("Shutdown complete.")

def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.APPLICATION_TITLE,
        description=settings.APPLICATION_DESCRIPTION,
        version=settings.APPLICATION_VERSION,
        debug=settings.ENVIRONMENT_DEBUG,
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT_DEBUG else None,
        redoc_url="/redoc" if settings.ENVIRONMENT_DEBUG else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT_DEBUG else None,
    )

    # Handlers
    register_exception_handlers(app)

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.ENVIRONMENT_DEBUG else settings.ALLOW_ORIGINS,
        allow_methods=["GET", "POST"],
        allow_headers=["X-API-Key", "Content-Type"],
    )

    if settings.APP_ENV == "PROD":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOST,  # mover a settings si quieres
        )

    # Routes
    app.include_router(
        api_router,
        prefix="/api/v1",
        dependencies=[Depends(api_key_auth)]
    )

    return app

try:
    app = create_app()
except Exception as e:
    logger.critical(f"Fatal error while starting FastAPI: {e}")
    sys.exit(1)