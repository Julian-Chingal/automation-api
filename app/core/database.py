import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

logger = logging.getLogger(__name__)
Base = declarative_base()

class DatabaseSessionManager:
    def __init__(self):
        self.engines = {}
        self.sessions = {}

    def init_databases(self, connections: dict):
        """Inicializa múltiples bases de datos desde un diccionario."""
        for name, uri in connections.items():
            if not uri:
                logger.warning(f"URI para '{name}' vacía. Saltando...")
                continue
            
            engine = create_engine(uri, pool_pre_ping=True, pool_size=5)
            self.engines[name] = engine

            factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
            self.sessions[name] = scoped_session(factory)
            logger.success(f"ORM vinculado a base de datos: {name.upper()}")

    def get_db(self, name: str):
        """Generador para dependencias de FastAPI."""
        session = self.sessions.get(name)
        if session is None:
            raise Exception(f"Base de datos '{name}' no inicializada")
        
        db = session()
        try:
            yield db
        finally:
            db.close()

db_manager = DatabaseSessionManager()