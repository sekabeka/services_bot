import pytest
import pytest_asyncio

from sqlalchemy import select
from datetime import datetime, timezone

from core.models import User, Service, Employee, Booking


@pytest.mark.asyncio
async def test_base_update_fields(session):
    old_firstname = "John"
    user = User(firstname=old_firstname)
    employee = Employee(firstname="test", lastname="test")
    service = Service(title="tes", duration=90)
    employee.services.append(service)
    booking = Booking(user=user, service=service, employee=employee, date=datetime.now().date())
    session.add_all([user, service, employee, booking])
    await session.commit()

    user.update_fields(firstname="Adam", lastname="Johnson")
    booking.update_fields(notified=True)

    query_for_user = select(User).filter(User.id == user.id)
    updated_user = (await session.execute(query_for_user)).scalars().first()

    query_for_booking = select(Booking).filter(Booking.id == booking.id)
    updated_booking = (await session.execute(query_for_booking)).scalars().first()

    assert updated_user.firstname == "Adam"
    assert updated_user.lastname == "Johnson"
    assert updated_booking.notified == True



@pytest.mark.skip
@pytest.mark.usefixtures("session")
class TestUserCases:
    ...

@pytest.mark.skip
@pytest.mark.usefixtures("session")
class TestEmployeeCases:
    async def test_all(self, session):
        employee = Employee(firstname="firstname", lastname="lastname")
        service = Service(title="title", duration=90)
        user = User(firstname="user_firstname")
        instances = [
            employee,
            user,
            service
        ]
        employee.services.append(service)
        employee.services.append(Service(title="title", duration=1231))
        session.add_all(instances)
        await session.commit()
        employees = await Employee.all()
        assert len(employees) == 1
        assert employee in employees
        await session.close()

        raise Exception(employee.services)

@pytest.mark.skip
@pytest.mark.usefixtures("session")
class TestBookingCases:
    async def test_fetch_bookings(self, session):
        employee = Employee(
            firstname="John",
            lastname="Anderson"
        )
        user = User(firstname="Gleb")
        service = Service(
            title="Massage",
            duration=120
        )
        employee.bookings.append(
            Booking(user=user, service=service, date=datetime.now())
        )
        employee.bookings.append(
            Booking(user=user, service=service, date=datetime.now())
        )
        employee.bookings.append(
            Booking(user=user, service=service, date=datetime.now())
        )

        employee_2 = Employee(firstname="test", lastname="test")
        employee_2.bookings.append(
            Booking(user=user, service=service, date=datetime.now())
        )
        session.add_all([employee, employee_2, user, service])
        await session.commit()

        bookings_for_employee = await Booking.fetch_bookings(employee_id=employee.id, date=datetime.now().date())
        assert len(bookings_for_employee) == 3

        bookings_for_employee_2 = await Booking.fetch_bookings(employee_id=employee_2.id, date=datetime.now().date())
        assert len(bookings_for_employee_2) == 1

    async def test_add_booking(self, session):
        emp = Employee(firstname="test", lastname="test")
        user = User(firstname="firstname")
        service = Service(title="title", duration=90)

        session.add_all([emp, user, service])
        await session.commit()
        now = datetime.now()
        booking = await Booking.add_booking(emp.id, user.id, service.id, now)

        assert booking is not None
        assert booking.id == 1
        assert booking.date == now.astimezone(timezone.utc)
        assert booking.user_id == user.id
        assert booking.employee_id == emp.id
        assert booking.service_id == service.id





