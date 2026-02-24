import threading
from contextlib import contextmanager
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.exceptions import DatabaseAliasNotRegisteredError


class DBManager:
    def __init__(self):
        self._engines: Dict[str, object] = {}
        self._sessions: Dict[str, object] = {}  # guarda session factories
        self._lock = threading.Lock()

    def _get_or_create_engine(self, alias: str, connection_url: str):
        with self._lock:
            if alias not in self._engines:
                engine = create_engine(
                    connection_url,
                    pool_size=10,
                    max_overflow=20,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    future=True,
                )
                # Engine y session factory en sus dicts 
                self._engines[alias] = engine
                self._sessions[alias] = sessionmaker(
                    bind=engine,
                    autoflush=False,
                    autocommit=False,
                )

        return self._engines[alias]

    def register(self, alias: str, connection_url: str):
        """Registra una base de datos con un alias."""
        self._get_or_create_engine(alias, connection_url)

    @contextmanager
    def get_session(self, alias: str): 
        """Context manager que entrega una sesión lista con commit/rollback automático."""
        if alias not in self._sessions:
            raise DatabaseAliasNotRegisteredError(alias)

        session = self._sessions[alias]()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_engine(self, alias: str):
        """Devuelve el engine asociado al alias (útil para pandas to_sql)."""
        if alias not in self._engines:
            raise DatabaseAliasNotRegisteredError(alias)
        return self._engines[alias]

    def dispose(self, alias: str):
        """Cierra y limpia el engine y su session factory."""
        with self._lock:
            if alias in self._engines:
                self._engines[alias].dispose()
                del self._engines[alias]
            if alias in self._sessions:
                del self._sessions[alias]

    def dispose_all(self):
        """Cierra y limpia todos los engines y session factories."""
        for alias in list(self._engines.keys()):
            self.dispose(alias)