from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker, ListRedisScheduleSource

from ...config import get_config
from ..common import StructuredLogger
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
