from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ...config import get_config
from ..common import StructuredLogger

config = get_config()


class Database:
    """
    Class for controlling the connection to the database, using SQLAlchemy.
    Provides methods for initializing, receiving sessions, and closing connections.
    """

    _engine: AsyncEngine | None = None
    _SessionLocal: async_sessionmaker | None = None

    @classmethod
    async def init(cls) -> None:
        """
        Initializes the database, creating an engine and a session factory.
        """
        if cls._engine is None:
            cls._engine = create_async_engine(
                config.database_url,
                echo=False,
                future=True,
                pool_size=20,  # minimal amount of connections in the pool
                max_overflow=10,  # additional connections beyond pool_size, if necessary
                pool_timeout=10,  # expected time of successful connection createion (in seconds)
                pool_use_lifo=True,
            )

            @event.listens_for(cls._engine.sync_engine, "connect")
            def enable_sqlite_fk(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

            cls._SessionLocal = async_sessionmaker(
                bind=cls._engine, class_=AsyncSession, expire_on_commit=False
            )
            StructuredLogger.info("database_initialized")

    @classmethod
    @asynccontextmanager
    async def get_session(cls) -> AsyncGenerator[AsyncSession, Any]:
        """
        Creates and returns an asynchronous SQLAlchemy session.
        Used inside the async with context manager.
        """
        if cls._SessionLocal is None:
            raise RuntimeError(
                "Database is not initialized. Call Database.init() first."
            )

        async with cls._SessionLocal() as session:
            StructuredLogger.info("session_created")
            async with session.begin():
                yield session  # the session is created here

    @classmethod
    async def dependency(cls) -> AsyncGenerator[AsyncSession, Any]:
        """
        Dependency for FastAPI - gives away the DB session.
        Used in Depends(get_db_session).
        """
        async with cls.get_session() as session:
            yield session

    @classmethod
    async def close(cls) -> None:
        """
        Closes the connection to the database
        """
        if cls._engine:
            await cls._engine.dispose()
            StructuredLogger.info("database.closed")

    @classmethod
    async def test_connection(cls) -> bool:
        """
        Tests the connection to the database
        """
        try:
            async with cls.get_session() as session:
                await session.execute(text("SELECT 1"))
            StructuredLogger.info("database_connection_successful")
            return True
        except Exception as e:
            StructuredLogger.exception("database_connection_failed", error=str(e))
            return False
