import asyncio
import time

from loguru import logger
from aiogram.enums import ParseMode

from settings import OWNER
from core.bot import bot
from core.celery_app.celery import app
from core.database import get_records_for_notifications
from core.templates import NOTIFY_TEMPLATE_FOR_OWNER, NOTIFY_TEMPLATE_FOR_USER

loop = asyncio.get_event_loop()

@app.task
def send_to_clients():
    records = get_records_for_notifications()
    for record in records:
        try:
            loop.run_until_complete(
                bot.send_message(
                    record.client,
                    text=NOTIFY_TEMPLATE_FOR_USER.format(
                        id=record.id, title=record.service.title, date=record.date
                    ),
                    parse_mode=ParseMode.HTML,
                )
            )
        except Exception as e:
            logger.error(str(e))
        record.notified = True
        record.save()
        time.sleep(1/30)


@app.task
def send_to_owner(id, title, date):
    try:
        loop.run_until_complete(bot.send_message(
            chat_id=OWNER,
            text=NOTIFY_TEMPLATE_FOR_OWNER.format(
                id=id,
                title=title,
                date=date
            ),
            parse_mode=ParseMode.HTML
        ))
    except Exception as e:
        logger.error(str(e))

app.conf.beat_schedule = {
    "send_to_clients": {
        "task": "core.celery_app.tasks.send_to_clients",
        "schedule": 60 * 60,
    }
}
