from datetime import datetime, timedelta, date, timezone

import pytest
import pytest_asyncio

from core.utils import get_available_bookings, get_bookings_for_notifications
from core.models import User, Employee, Service, Booking

@pytest_asyncio.fixture(autouse=True)
async def setup(session):
    emp = Employee(
        firstname="firstname",
        lastname="lastname"
    )
    user = User(tg_id=190312)
    service = Service(
        title="title",
        duration=90
    )
    session.add_all([emp, service, user])
    await session.commit()
    yield
    await session.rollback()

@pytest.mark.asyncio
async def test_available_bookings(session):
    year, month, day = 2025, 1, 1
    date1 = datetime(year, month, day, 9, 0)
    date2 = datetime(year, month, day, 12, 0)
    date3 = datetime(year, month, day, 18, 0)

    await Booking.add_booking(1, 1, 1, date1)
    await Booking.add_booking(1, 1, 1, date2)
    await Booking.add_booking(1, 1, 1, date3)

    free_bookings = await get_available_bookings(
        date(year, month, day),
        90, 1
    )

    expected_result = [
        (datetime(year, month, day, 10, 30), datetime(year, month, day, 12, 0)),
        (datetime(year, month, day, 13, 30), datetime(year, month, day, 15, 0)),
        (datetime(year, month, day, 15, 0), datetime(year, month, day, 16, 30)),
        (datetime(year, month, day, 16, 30), datetime(year, month, day, 18, 0)),
        (datetime(year, month, day, 19, 30), datetime(year, month, day, 21, 0))
    ]
    assert expected_result == free_bookings


@pytest.mark.asyncio
async def test_bookings_for_notifications(session):
    now = datetime.now()

    date1 = now + timedelta(hours=10)
    date2 = now + timedelta(days=2)
    date3 = now - timedelta(minutes=12)

    await Booking.add_booking(1, 1, 1, date1)
    await Booking.add_booking(1, 1, 1, date2)
    await Booking.add_booking(1, 1, 1, date3)

    result = await get_bookings_for_notifications(session)

    assert len(result) == 1


