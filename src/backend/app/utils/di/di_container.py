from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq_redis import ListQueueBroker, ListRedisScheduleSource

from ...config import get_config
from ..common import StructuredLogger
from ..db import Database
from .di_providers import (
    AsyncClientProvider,
    ClickFunnelsClientProvider,
    DBSessionProvider,
    ServiceProvider,
    TwilioClientProvider,
)

config = get_config()

StructuredLogger.setup()

_schedule_source_ready = False


async def ensure_schedule_source_ready() -> None:
    global _schedule_source_ready
    if not _schedule_source_ready:
        await schedule_source.startup()
        _schedule_source_ready = True


broker = ListQueueBroker(url=config.REDIS_URL)
schedule_source = ListRedisScheduleSource(url=config.REDIS_URL)
scheduler = TaskiqScheduler(broker=broker, sources=[schedule_source])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    await Database.init()
    await Database.test_connection()
    StructuredLogger.info("worker.started")


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def on_worker_shutdown(state: TaskiqState) -> None:
    await Database.close()
    StructuredLogger.info("worker.stopped")


container = make_async_container(
    AsyncClientProvider(),
    ClickFunnelsClientProvider(),
    DBSessionProvider(),
    ServiceProvider(),
    TwilioClientProvider(
        account_sid=config.TWILIO_ACCOUNT_SID,
        auth_token=config.TWILIO_AUTH_TOKEN,
        from_number=config.TWILIO_FROM_NUMBER,
    ),
)


setup_dishka(container=container, broker=broker)

# from ..taskiq import tasks  # noqa
