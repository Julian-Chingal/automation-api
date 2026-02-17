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
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'localhost:5432/devdb')

class ProductionConfig(Config):
    DEBUG = False
    REQUIRED_VARS = ["DATABASE_URI"]
    
    DATABASE_URI = os.environ.get('DATABASE_URI')