from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from .redis_client import RedisClient
from .structured_logger import StructuredLogger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Context manager for controlling the lifespan of the FastAPI app.
    Initializes and closes resources at the start and the end of the app.
    """
    try:
        await RedisClient.init()
        yield
    except Exception as e:
        StructuredLogger.exception("init.error", error=str(e))
        raise e
    finally:
        await app.state.dishka_container.close()
        await RedisClient.close()
