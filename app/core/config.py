import os

class Config:
    """Clase base de configuración."""
    PORT = int(os.environ.get('PORT', 8000))
    REQUIRED_VARS = []

    @classmethod
    def validate(cls):
        """Verifica que todas las variables requeridas estén presentes."""
        missing = [var for var in cls.REQUIRED_VARS if not os.environ.get(var)]
        if missing:
            raise EnvironmentError(
                f"Faltan las siguientes variables de entorno: {', '.join(missing)}"
            )

class DevelopmentConfig(Config):
    DEBUG = True

    @classmethod
    def get_db_connections(cls):
        return {
            "erc": os.environ.get('DB_ERC_URI')
        }

class ProductionConfig(Config):
    DEBUG = False
    REQUIRED_VARS = ["DB_ERC_URI"]

    @classmethod
    def get_db_connections(cls):
        return {
            "erc": os.environ.get('DB_ERC_URI')
        }