from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from dishka.integrations.taskiq import FromDishka, inject

from ...config import RegisterType, SmsTemplate, get_config
from ..clickfunnels import ClickFunnelsClient, ClickFunnelsUtils
from ..common import StructuredLogger
from ..di import broker, ensure_schedule_source_ready, schedule_source
from ..models import WorkflowBuilder
from ..services import WebhookEventService
from ..twilio import TwilioClient

config = get_config()


@broker.task(task_name="clickfunnels.process_webhook")
@inject(patch_module=True)
async def process_clickfunnels_webhook(
    payload: dict,
    clickfunnels_client: FromDishka[ClickFunnelsClient],
    webhook_event_service: FromDishka[WebhookEventService],
) -> None:
    if config.LOG_RAW_PAYLOAD:
        StructuredLogger.info(
            "request.raw_payload",
            payload=payload,
        )

    event_id = payload.get("event_id")

    if event_id is None:
        StructuredLogger.error(
            "request.event_id.not_found",
            payload=payload,
        )
        return None

    try:
        event_id = UUID(event_id)

    except Exception:
        StructuredLogger.error(
            "request.event_id.invalid",
            event_id=event_id,
        )
        return None

    created = await webhook_event_service.create_if_not_exists(event_id)
    if not created:
        StructuredLogger.warning(
            "tasks.clickfunnels.process_webhook.event_already_exists",
            event_id=event_id,
        )
        return None

    StructuredLogger.info("tasks.clickfunnels.process_webhook.event_created")

    contact = ClickFunnelsUtils.extract_contact(payload)
    StructuredLogger.info(
        "tasks.clickfunnels.process_webhook.contact_extracted",
        contact=contact,
        contact_id=contact.id,
    )

    page_context = ClickFunnelsUtils.resolve_page(contact.page_name)
    if page_context is None:
        StructuredLogger.error(
            "tasks.clickfunnels.process_webhook.unsupported_page",
            page_name=contact.page_name,
        )
        return None

    now = datetime.now(tz=page_context.timezone)

    if page_context.register_type == RegisterType.TODAY:
        webinar_time = now.replace(hour=page_context.web_start_hour)

        if now > webinar_time:
            plan = WorkflowBuilder.build_tomorrow(page_context.workflow_definition, now)
            StructuredLogger.warning(
                "tasks.clickfunnels.process_webhook.register_today_delay_until_tomorrow",
                now=now,
                webinar_time=webinar_time,
            )

        else:
            plan = WorkflowBuilder.build_today(page_context.workflow_definition, now)

        await clickfunnels_client.update_or_create_contact(
            body={
                "contact": {
                    "custom_attributes": plan.custom_attributes,
                    "email_address": contact.email,
                    "phone_number": contact.phone_number,
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                },
            },
        )

    elif page_context.register_type == RegisterType.TOMORROW:
        plan = WorkflowBuilder.build_tomorrow(page_context.workflow_definition, now)

    else:
        StructuredLogger.error(
            "tasks.clickfunnels.process_webhook.unresolved_register_type",
            page_context=page_context,
        )

    StructuredLogger.info(
        "tasks.clickfunnels.process_webhook.page_context_resolved",
        page_context=page_context,
    )

    StructuredLogger.info(
        "tasks.clickfunnels.process_webhook.plan_built",
        plan=plan,
        sms_count=len(plan.sms_templates),
    )

    if contact.phone_number is not None:
        await send_sms_task.kiq(
            phone_number=contact.phone_number,
            template=page_context.welcome_sms_template,
        )  # type: ignore

        StructuredLogger.info(
            "tasks.clickfunnels.process_webhook.welcome_sms_sent",
            phone_number=contact.phone_number,
            template=page_context.welcome_sms_template,
        )

        await schedule_sms_templates(
            phone_number=contact.phone_number,
            items=plan.sms_templates,
            timezone=page_context.timezone,
        )

        StructuredLogger.info(
            "tasks.clickfunnels.process_webhook.sms_scheduled",
            phone_number=contact.phone_number,
            items=plan.sms_templates,
            timezone=page_context.timezone,
        )

    else:
        StructuredLogger.warning(
            "tasks.clickfunnels.process_webhook.missing_phone_number",
            contact=contact,
        )

    StructuredLogger.info(
        "tasks.clickfunnels.process_webhook.processed_successfully",
        event_id=event_id,
    )


@broker.task(task_name="twilio.send_sms")
@inject(patch_module=True)
async def send_sms_task(
    phone_number: str,
    template: SmsTemplate,
    twilio_client: FromDishka[TwilioClient],
) -> None:
    await twilio_client.send_sms(
        to_phone=phone_number,
        template=template,
    )
    StructuredLogger.info(
        "tasks.twilio.send_sms.sms_sent",
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
