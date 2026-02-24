import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import Tuple, Type

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.v1.api import api_router
from core.handlers import register_exception_handlers
from core.config import Config, DevelopmentConfig, ProductionConfig
from core.db_manager import DBManager
from core.logger import configure_logging

# Inicialización de logs y entorno
load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)
db_manager = DBManager()

# Mapeo de entornos
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_validated_config() -> Tuple[Type[Config], str]:
    env = os.getenv("APP_ENV", "").lower()

    if not env:
        logger.critical("Variable 'APP_ENV' no definida. Valores válidos: development | production")
        sys.exit(1)

    if env not in CONFIG_MAP:
        logger.critical(f"Entorno '{env}' no válido. Opciones: {list(CONFIG_MAP.keys())}")
        sys.exit(1)

    config_class = CONFIG_MAP[env]

    try:
        config_class.validate()
        return config_class, env
    except EnvironmentError as e:
        logger.critical(f"Error de validación de variables de entorno: {e}")
        sys.exit(1)

def create_app() -> FastAPI:
    config, env_name = get_validated_config()

    # ── Lifespan ──────────────────────────────
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info(f"Iniciando en entorno: {env_name.upper()}")

        # Registrar conexiones a bases de datos
        for alias, url in config.get_db_connections().items():
            try:
                db_manager.register(alias, url)
                logger.info(f"DB registrada: [{alias}]")
            except Exception as e:
                logger.critical(f"No se pudo conectar la DB '{alias}': {e}")
                sys.exit(1)

        # Exponer db_manager en el estado de la app (para dependency injection)
        app.state.db_manager = db_manager

        logger.info("App lista para recibir requests.")
        yield

        # Shutdown limpio
        logger.info("Cerrando conexiones a bases de datos...")
        db_manager.dispose_all()
        logger.info("Shutdown completo.")

    # ── Instancia FastAPI ─────────────────────
    app = FastAPI(
        title="API Automatización de Procesos",
        version="1.0.0",
        debug=config.DEBUG,
        lifespan=lifespan,
        docs_url="/docs" if env_name == "development" else None,
        redoc_url="/redoc" if env_name == "development" else None,
        openapi_url="/openapi.json" if env_name == "development" else None,
    )

    #----Global Handlers------------------------
    register_exception_handlers(app)

    # ── Middlewares ───────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_ORIGINS,
        allow_methods=["GET", "POST"],
        allow_headers=["X-API-Key", "Content-Type"],
    )

    if env_name == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=config.ALLOWED_HOSTS,
        )

    # ── Rutas ─────────────────────────────────
    app.include_router(api_router, prefix="/api/v1")

    return app

#* ------------------------------
#* Entry point
#* ------------------------------
try:
    app = create_app()
except Exception as e:
    logger.critical(f"Fallo catastrófico al instanciar FastAPI: {e}")
    sys.exit(1)
