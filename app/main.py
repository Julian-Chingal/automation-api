import logging
import os
import sys
from typing import Tuple, Type

from dotenv import load_dotenv
from fastapi import FastAPI

from api.v1.api import api_router
from core.config import Config, DevelopmentConfig, ProductionConfig
from core.logger import configure_logging
from core.database import db_manager

# Inicialización de logs y entorno
load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)

# Mapeo de entornos
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_validated_config() -> Tuple[Type[Config], str]:
    """Valida el entorno y devuelve la clase de configuración activa."""
    env = os.getenv("APP_ENV", "").lower()
    
    if not env:
        logger.critical("❌ Variable 'APP_ENV' no definida (development/production).")
        sys.exit(1)

    if env not in CONFIG_MAP:
        logger.critical(f"❌ Entorno '{env}' no es válido. Opciones: {list(CONFIG_MAP.keys())}")
        sys.exit(1)

    config_class = CONFIG_MAP[env]
    
    try:
        config_class.validate()
        return config_class, env
    except EnvironmentError as e:
        logger.critical(f"❌ Error de validación: {e}")
        sys.exit(1)

def create_app() -> FastAPI:
    """Fábrica de la aplicación FastAPI."""
    config, env_name = get_validated_config()
    db_manager.init_databases(config.get_db_connections())
    
    app = FastAPI(
        title="API Automatizacion de Procesos",
        debug=getattr(config, "DEBUG", False),
        version="1.0.0"
    )

    # Rutas
    app.include_router(api_router, prefix="/api")
    
    logger.success(f"🚀 App lista | Entorno: {env_name.upper()} | Debug: {app.debug}")
    return app

try:
    app = create_app()
except Exception as e:
    logger.critical(f"Fallo catastrófico al instanciar FastAPI: {e}")
    sys.exit(1)
