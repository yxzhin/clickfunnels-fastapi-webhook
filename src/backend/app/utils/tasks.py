from datetime import datetime
from zoneinfo import ZoneInfo

from dishka.integrations.taskiq import FromDishka, inject
from httpx import AsyncClient
from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker, ListRedisScheduleSource

from ..config import RegisterType, SmsTemplate, get_config
from .clickfunnels_client import ClickFunnelsClient
from .clickfunnels_utils import ClickFunnelsUtils
from .helpers import Helpers
from .structured_logger import StructuredLogger
from .twilio_client import TwilioClient
from .workflows import WorkflowBuilder

config = get_config()
broker = ListQueueBroker(url=config.REDIS_URL)
schedule_source = ListRedisScheduleSource(url=config.REDIS_URL)
scheduler = TaskiqScheduler(broker=broker, sources=[schedule_source])

_schedule_source_ready = False


async def ensure_schedule_source_ready() -> None:
    global _schedule_source_ready
    if not _schedule_source_ready:
        await schedule_source.startup()
        _schedule_source_ready = True


@broker.task(task_name="clickfunnels.process_webhook")
@inject(patch_module=True)
async def process_clickfunnels_webhook(
    payload: dict,
    page_hint: str,
    now: datetime,
    httpx_client: FromDishka[AsyncClient],
) -> None:
    contact = ClickFunnelsUtils.extract_contact(payload)
    page_context = ClickFunnelsUtils.resolve_page(payload, page_hint)
    if page_context is None:
        StructuredLogger.warning(
            "clickfunnels.process_webhook.unsupported_page", page_hint=page_hint
        )
        return None

    twilio = TwilioClient()
    cf = ClickFunnelsClient(httpx_client)

    if contact.has_phone:
        await twilio.send_sms(
            to_phone=contact.phone_number or "",
            template=page_context.welcome_sms_template,
        )
    else:
        StructuredLogger.warning("clickfunnels.process_webhook.missing_phone_number")

    if page_context.register_type == RegisterType.TODAY:
        plan = WorkflowBuilder.build_today(page_context.workflow_definition, now)
        await cf.upsert_contact(
            contact_id=contact.id,
            body={
                "custom_attributes": plan.custom_attributes,
                # "email_address": contact.email,
                # "phone_number": contact.phone_number,
                # "first_name": contact.first_name,
                # "last_name": contact.last_name,
            },
        )

    elif page_context.register_type == RegisterType.TOMORROW:
        plan = WorkflowBuilder.build_tomorrow(page_context.workflow_definition, now)

    await schedule_sms_templates(
        contact.phone_number, plan.sms_templates, page_context.timezone
    )


@broker.task(task_name="clickfunnels.send_sms")
async def send_sms_task(phone_number: str | None, template_name: str) -> None:
    if not phone_number or not Helpers.trim(phone_number):
        StructuredLogger.warning("tasks.clickfunnels.send_sms.missing_phone_number")
        return

    twilio = TwilioClient()
    template = SmsTemplate(template_name)
    await twilio.send_sms(to_phone=phone_number, template=template)


async def schedule_sms_templates(
    phone_number: str | None,
    items: list[tuple[SmsTemplate, datetime]],
    timezone: ZoneInfo,
) -> None:
    if not phone_number or not Helpers.trim(phone_number):
        StructuredLogger.warning("tasks.schedule_sms_templates.missing_phone_number")
        return

    await ensure_schedule_source_ready()

    for template, when in items:
        await send_sms_task.schedule_by_time(
            schedule_source,
            when.astimezone(timezone),
            phone_number,
            template.value,
        )
