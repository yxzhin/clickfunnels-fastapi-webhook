from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio import Redis, lock
from redis.asyncio.connection import ConnectionPool

from ...config import get_config
from ..common import StructuredLogger

config = get_config()


class RedisClient:
    """
    Class for managing Redis connection.
    Provides methods to initialize and close connection.
    """

    _pool: ConnectionPool | None = None
    _client: Redis | None = None

    @classmethod
    async def init(cls) -> None:
        """Initialize Redis connection pool."""

        if cls._client is not None:
            return

        cls._pool = ConnectionPool.from_url(
            config.REDIS_URL,
            max_connections=20,
            socket_timeout=5,
            socket_connect_timeout=5,
            decode_responses=True,
        )
        cls._client = Redis(connection_pool=cls._pool)

        try:
            if await cls.ping():
                StructuredLogger.info("redis.connected")
        except Exception as e:
            StructuredLogger.exception("redis.connection_error", error=str(e))
            raise e

    @classmethod
    async def close(cls) -> None:
        """Close Redis connection."""

        if cls._client is not None:
            await cls._client.aclose()
            cls._client = None
            StructuredLogger.info("redis.client.closed")

        if cls._pool is not None:
            await cls._pool.disconnect(inuse_connections=True)
            cls._pool = None
            StructuredLogger.info("redis.pool.closed")

    @classmethod
    def _require_client(cls) -> Redis:
        if cls._client is None:
            raise RuntimeError("Redis client is not initialized. Call connect() first.")
        return cls._client

    @classmethod
    async def ping(cls) -> bool:
        client = cls._require_client()
        return bool(await client.ping())  # type: ignore

    @classmethod
    async def get(cls, key: str) -> str | None:
        client = cls._require_client()
        return await client.get(key)

    @classmethod
    async def set(
        cls,
        key: str,
        value: str,
        *,
        ex: int | None = None,
        px: int | None = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        client = cls._require_client()
        return bool(await client.set(key, value, ex=ex, px=px, nx=nx, xx=xx))

    @classmethod
    async def delete(cls, *keys: str) -> int:
        client = cls._require_client()
        return int(await client.delete(*keys))

    @classmethod
    async def expire(cls, key: str, seconds: int) -> bool:
        client = cls._require_client()
        return bool(await client.expire(key, seconds))

    @classmethod
    async def ttl(cls, key: str) -> int:
        client = cls._require_client()
        return int(await client.ttl(key))

    @classmethod
    async def incr(cls, key: str, amount: int = 1) -> int:
        client = cls._require_client()
        return int(await client.incrby(key, amount))

    @classmethod
    async def set_json(cls, key: str, value: Any, *, ex: int | None = None) -> bool:
        import json

        return await cls.set(key, json.dumps(value, ensure_ascii=False), ex=ex)

    @classmethod
    async def get_json(cls, key: str) -> Any:
        import json

        raw = await cls.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    @classmethod
    @asynccontextmanager
    async def lock(
        cls,
        name: str,
        *,
        timeout: int = 10,
        blocking_timeout: int = 5,
    ) -> AsyncIterator[lock.Lock]:
        client = cls._require_client()
        lock = client.lock(name, timeout=timeout, blocking_timeout=blocking_timeout)
        async with lock:
            yield lock
