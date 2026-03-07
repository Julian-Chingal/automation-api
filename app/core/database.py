from contextlib import contextmanager
from .settings import settings
from threading import Lock
from typing import Dict
import logging

from core.exceptions import DatabaseAliasNotRegisteredError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self):
        self._engines: Dict[str, Engine] = {}
        self._session_factories: Dict[str, sessionmaker] = {} 
        self._lock = Lock()

    # Internal
    def _create_engine(self, alias: str):
        if alias not in settings.DATABASES:
            raise DatabaseAliasNotRegisteredError(alias)

        uri = settings.DATABASES[alias]

        pool_size = 5 if settings.APP_ENV == "DEV" else 15
        max_overflow = 10 if settings.APP_ENV == "DEV" else 30

        engine = create_engine(
            uri,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
            pool_recycle=1800,
            future=True
        )

        self._engines[alias] = engine

        self._session_factories[alias] = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

        logger.info(f"[DBManager] Engine created for alias: {alias}")

    def _ensure_engine(self, alias: str):
        if alias not in self._engines:
            with self._lock:
                if alias not in self._engines:
                    self._create_engine(alias)
    
    # Public 
    @contextmanager
    def get_session(self, alias: str): 
        """Context manager que entrega una sesión lista con commit/rollback automático."""
        self._ensure_engine(alias)

        session = self._session_factories[alias]()

        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.exception(
                f"[DBManager] Transaction rollback in alias '{alias}'"
            )
            raise
        finally:
            session.close()

    def get_engine(self, alias: str):
        """Devuelve el engine asociado al alias (útil para pandas to_sql)."""
        self._ensure_engine(alias)
        return self._engines[alias]

    def health_check(self) -> dict:
        """
        Verifica conectividad básica a todas las DB configuradas.
        """
        status = {}

        for alias in settings.DATABASES.keys():
            try:
                engine = self.get_engine(alias)
                with engine.connect() as conn:
                    conn.execute("SELECT 1")
                status[alias] = "OK"
            except Exception:
                status[alias] = "ERROR"

        return status

    def dispose_all(self):
        for alias, engine in self._engines.items():
            engine.dispose()
        self._engines.clear()
        self._session_factories.clear()
        
db_manager = DBManager()