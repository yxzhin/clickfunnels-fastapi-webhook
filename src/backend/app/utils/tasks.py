from datetime import datetime
from zoneinfo import ZoneInfo

from dishka.integrations.taskiq import FromDishka, inject

from ..config import RegisterType, SmsTemplate
from .clickfunnels_client import ClickFunnelsClient
from .clickfunnels_utils import ClickFunnelsUtils
from .di_container import broker, ensure_schedule_source_ready, schedule_source
from .structured_logger import StructuredLogger
from .twilio_client import TwilioClient
from .workflows import WorkflowBuilder


@broker.task(task_name="clickfunnels.process_webhook")
@inject(patch_module=True)
async def process_clickfunnels_webhook(
    payload: dict,
    clickfunnels_client: FromDishka[ClickFunnelsClient],
) -> None:
    contact = ClickFunnelsUtils.extract_contact(payload)
    StructuredLogger.info(
        "tasks.clickfunnels.process_webhook.contact_extracted",
        contact=contact,
        contact_id=contact.id,
    )

    page_context = ClickFunnelsUtils.resolve_page(contact.page_name)
    if page_context is None:
        StructuredLogger.warning(
            "clickfunnels.process_webhook.unsupported_page",
        )
        return None

    now = datetime.now(tz=page_context.timezone)

    if page_context.register_type == RegisterType.TODAY:
        plan = WorkflowBuilder.build_today(page_context.workflow_definition, now)
        await clickfunnels_client.update_or_create_contact(
            contact_id=contact.id,
            body={
                "custom_attributes": plan.custom_attributes,
                "email_address": contact.email,
                "phone_number": contact.phone_number,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
            },
        )

    elif page_context.register_type == RegisterType.TOMORROW:
        plan = WorkflowBuilder.build_tomorrow(page_context.workflow_definition, now)

    else:
        StructuredLogger.warning(
            "tasks.clickfunnels.process_webhook.unresolved_register_type",
            page_context=page_context,
        )

    StructuredLogger.warning(
        "tasks.clickfunnels.process_webhook.page_context_resolved",
        page_context=page_context,
    )

    StructuredLogger.info(
        "tasks.clickfunnels.process_webhook.plan_built",
        plan=plan,
    )

    if contact.phone_number is not None:
        await send_sms_task.kiq(
            phone_number=contact.phone_number,
            template=page_context.welcome_sms_template,
        )  # type: ignore
        StructuredLogger.info("tasks.clickfunnels.process_webhook.welcome_sms_sent")
        await schedule_sms_templates(
            phone_number=contact.phone_number,
            items=plan.sms_templates,
            timezone=page_context.timezone,
        )
        StructuredLogger.info("tasks.clickfunnels.process_webhook.sms_scheduled")

    else:
        StructuredLogger.warning(
            "tasks.clickfunnels.process_webhook.missing_phone_number",
            contact_id=contact.id,
            page_context=page_context,
        )


@broker.task(task_name="clickfunnels.send_sms")
@inject(patch_module=True)
async def send_sms_task(
    phone_number: str,
    template: SmsTemplate,
    twilio_client: FromDishka[TwilioClient],
) -> None:
    await twilio_client.send_sms(to_phone=phone_number, template=template)
    StructuredLogger.info(
        "tasks.clickfunnels.send_sms.sms_sent",
        to_phone=phone_number,
        template=template,
    )


async def schedule_sms_templates(
    phone_number: str,
    items: list[tuple[SmsTemplate, datetime]],
    timezone: ZoneInfo,
) -> None:
    await ensure_schedule_source_ready()

    for template, when in items:
        await send_sms_task.schedule_by_time(
            source=schedule_source,
            time=when.astimezone(timezone),
            phone_number=phone_number,
            template=template,
        )  # type: ignore
