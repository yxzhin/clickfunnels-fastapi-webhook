from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from fastapi import FastAPI

from ..di.providers import AsyncClientProvider
from .redis_client import RedisClient
from .structured_logger import StructuredLogger
from .tasks import broker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Context manager for controlling the lifespan of the FastAPI app.
    Initializes and closes resources at the start and the end of the app.
    """
    StructuredLogger.setup()
    try:
        container = make_async_container(
            AsyncClientProvider(),
        )
        setup_dishka(container=container, broker=broker)
        await RedisClient.init()
        yield
    except Exception as e:
        StructuredLogger.exception("init.error", error=str(e))
        raise e
    finally:
        await container.close()
        await RedisClient.close()
