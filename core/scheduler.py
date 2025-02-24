import asyncio

from loguru import logger
from aiogram.enums import ParseMode
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.bot import bot
from jinja2 import Template
from settings import TIMEZONE
from core.database import async_session_factory
from core.utils import (
    get_bookings_for_notifications,
    get_employees_with_bookings
)

from core.templates import (
    NOTIFY_TEMPLATE_FOR_USER,
    NOTIFY_TEMPLATE_FOR_EMPLOYEE_MORNING
)

scheduler = AsyncIOScheduler()

async def send_to_users():
    async with async_session_factory() as session:
        bookings = await get_bookings_for_notifications(session)
        for booking in bookings:
            try:
                await bot.send_message(
                    chat_id=booking.user.tg_id,
                    text=NOTIFY_TEMPLATE_FOR_USER.format(
                        id=booking.id, title=booking.service.title,
                        date=booking.date
                    ),
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                logger.error(e)

            await booking.update_fields(notified=True)
            await session.commit()
            await asyncio.sleep(1/30)
            logger.info(f"Send notify to {booking.user.username}")

async def send_to_employees_today():
    employees = await get_employees_with_bookings()
    for employee in employees:
        try:
            bookings = employee.bookings
            text = Template(NOTIFY_TEMPLATE_FOR_EMPLOYEE_MORNING).render(bookings=bookings)
            await bot.send_message(
                chat_id=employee.tg_id,
                text=text,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(e)

trigger = CronTrigger(
    hour=9,
    timezone=TIMEZONE
)

scheduler.add_job(send_to_users, "interval", hours=1)
scheduler.add_job(send_to_employees_today, trigger)




