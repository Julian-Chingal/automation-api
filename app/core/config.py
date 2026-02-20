import os
from typing import Dict, List

class Config:
    """Clase base de configuración."""
    PORT: int = int(os.environ.get('PORT', 8000))
    DEBUG: bool = False

    REQUIRED_VARS: List[str]= [
        "APP_ENV"
    ]

    DB_ENV_VARS: Dict[str, str] = {
        "erc": "DB_ERC_URI"
    }

    ALLOWED_ORIGINS: List[str] = []
    ALLOWED_HOSTS: List[str] = ["*"]

    @classmethod
    def validate(cls):
        """Verifica que todas las variables requeridas estén presentes."""
        missing = [var for var in cls.REQUIRED_VARS if not os.environ.get(var)]

        missing_db = [
            env_var
            for alias, env_var in cls.DB_ENV_VARS.items()
            if not os.environ.get(env_var)
        ]

        all_missing = missing + missing_db
        if all_missing:
            raise EnvironmentError(
                f"Faltan las siguientes variables de entorno: {', '.join(all_missing)}"
            )

    @classmethod
    def get_db_connections(cls) -> dict[str, str]:
        return {
            alias: os.environ.get(env_var)
            for alias, env_var in cls.DB_ENV_VARS.items()
        }

class DevelopmentConfig(Config):
    DEBUG = True
    ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

    DB_ENV_VARS = {
        "erc": "DB_ERC_URI"
    }

class ProductionConfig(Config):
    DEBUG = False
    ALLOWED_ORIGINS = []  
    ALLOWED_HOSTS = []    

    REQUIRED_VARS = [
        "API_KEY",
        "APP_ENV",
    ]

    DB_ENV_VARS = {
        "erc": "DB_ERC_URI",
    }