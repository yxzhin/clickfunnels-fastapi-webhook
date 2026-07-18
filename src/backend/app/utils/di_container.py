from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqMiddleware, TaskiqScheduler
from taskiq_redis import ListQueueBroker, ListRedisScheduleSource

from ..config import get_config
from .di_providers import (
    AsyncClientProvider,
    ClickFunnelsClientProvider,
    TwilioClientProvider,
)
from .structured_logger import StructuredLogger

config = get_config()

_schedule_source_ready = False


async def ensure_schedule_source_ready() -> None:
    global _schedule_source_ready
    if not _schedule_source_ready:
        await schedule_source.startup()
        _schedule_source_ready = True


class LoggingMiddleware(TaskiqMiddleware):
    async def pre_execute(self, message):
        StructuredLogger.setup()


broker = ListQueueBroker(url=config.REDIS_URL).with_middlewares(LoggingMiddleware())
schedule_source = ListRedisScheduleSource(url=config.REDIS_URL)
scheduler = TaskiqScheduler(broker=broker, sources=[schedule_source])


container = make_async_container(
    AsyncClientProvider(),
    ClickFunnelsClientProvider(),
    TwilioClientProvider(
        account_sid=config.TWILIO_ACCOUNT_SID,
        auth_token=config.TWILIO_AUTH_TOKEN,
        from_number=config.TWILIO_FROM_NUMBER,
    ),
)


setup_dishka(container=container, broker=broker)

from . import tasks  # noqa
