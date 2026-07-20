from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from ..common import StructuredLogger
from ..db import Database
from ..redis import RedisClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Context manager for controlling the lifespan of the FastAPI app.
    Initializes and closes resources at the start and the end of the app.
    """
    try:
        await Database.init()
        await Database.test_connection()
        await RedisClient.init()
        yield
    except Exception as e:
        StructuredLogger.exception("init.error", error=str(e))
        raise e
    finally:
        await app.state.dishka_container.close()
        await Database.close()
        await RedisClient.close()
