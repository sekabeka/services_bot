from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from aiogram.enums import ParseMode
from datetime import timedelta, datetime, date
from intervaltree import IntervalTree, Interval

from core.bot import bot
from core.database import async_session_factory
from core.models import Booking, Employee, User
from core.templates import NOTIFY_TEMPLATE_FOR_EMPLOYEE
from settings import START_TIME_OF_WORK, END_TIME_OF_WORK


async def get_available_bookings(booking_date, duration, employee_id):
    start = datetime.combine(booking_date, START_TIME_OF_WORK)
    end = datetime.combine(booking_date, END_TIME_OF_WORK)

    occupied_tree = IntervalTree()
    bookings = await Booking.fetch_bookings(booking_date, employee_id=employee_id)
    for booking in bookings:
        occupied_tree.add(
            Interval(
                booking.date.timestamp(),
                (
                    booking.date + timedelta(minutes=duration)
                ).timestamp(),
            )
        )

    free_bookings = []
    current_start = start.timestamp()
    end_timestamp = end.timestamp()
    duration_seconds = duration * 60
    while current_start + duration_seconds <= end_timestamp:
        current_end = current_start + duration_seconds
        overlapping_intervals = occupied_tree.overlap(current_start, current_end)
        if not overlapping_intervals:
            free_bookings.append(
                (
                    datetime.fromtimestamp(current_start),
                    datetime.fromtimestamp(current_end),
                )
            )
            current_start += duration_seconds
        else:
            last_end = max(interval.end for interval in overlapping_intervals)
            current_start = last_end

    return free_bookings

async def get_bookings_for_notifications(session=None):
    _datetime = datetime.now()
    query = (
        select(Booking)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.service),
            joinedload(Booking.employee)
        )
        .filter(
            Booking.date <= (_datetime + timedelta(days=1)),
            Booking.date >= _datetime,
            Booking.notified == False
        )
    )
    result = await session.execute(query)
    return result.unique().scalars().all()

async def send_to_employee_notify(employee_id, booking_id, title, date):
    try:
        await bot.send_message(
            chat_id=employee_id,
            text=NOTIFY_TEMPLATE_FOR_EMPLOYEE.format(
                id=booking_id,
                title=title,
                date=date
            ),
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(e)

async def get_employees_with_bookings():
    async with async_session_factory() as session:
        query = (
            select(Employee)
            .join(Booking)
            .filter(
                func.DATE(Booking.date) == datetime.now().date()
            )
            .options(
                joinedload(Employee.bookings)
            )
            .order_by(Booking.date)
        )
        result = await session.execute(query)
        return result.unique().scalars().all()

async def fetch_bookings(user_id):
    async with async_session_factory() as session:
        query = (
            select(Employee)
            .filter(
                Employee.tg_id == user_id
            )
        )
        employee = (await session.execute(query)).scalars().first()
        if employee:
            query = (
                select(Booking)
                .options(
                    joinedload(Booking.service),
                    joinedload(Booking.user),
                    joinedload(Booking.employee)
                )
                .filter(
                    Booking.employee.has(Employee.tg_id == employee.tg_id),
                    Booking.date >= datetime.now()
                )
                .order_by(Booking.date)
            )
        else:
            query = (
                select(Booking)
                .options(
                    joinedload(Booking.service),
                    joinedload(Booking.user),
                    joinedload(Booking.employee)
                )
                .filter(
                    Booking.user.has(User.tg_id == user_id),
                    Booking.date >= datetime.now()
                )
                .order_by(Booking.date)
            )
        result = await session.execute(query)
        return result.unique().scalars().all()







