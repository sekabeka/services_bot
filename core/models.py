from datetime import datetime, timezone
from decimal import Decimal

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Numeric
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database import async_session_factory, Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[Optional[str]] = mapped_column(String(64))
    lastname: Mapped[Optional[str]] = mapped_column(String(64))
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")
    username: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    tg_id: Mapped[Optional[int]]

    @classmethod
    async def get_or_create(cls, tg_id, **kwargs):
        async with async_session_factory() as session:
            result = await session.execute(
                select(cls).filter(cls.tg_id == tg_id)
            )
            user = result.scalars().first()
            if user:
                return user

            kwargs["tg_id"] = tg_id
            new_user = await cls.create(**kwargs)
            return new_user

    def __repr__(self) -> str:
        return f"User(tg_id={self.tg_id!r}, username={self.username!r})"

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(64))
    lastname: Mapped[str] = mapped_column(String(64))
    username: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    tg_id: Mapped[Optional[int]]
    description: Mapped[Optional[str]]
    services: Mapped[List["Service"]] = relationship(
        secondary="employee_services", back_populates="employees"
    )
    service_associations: Mapped[List["EmployeeServices"]] = relationship(
        back_populates="employee"
    )
    bookings: Mapped[List["Booking"]] = relationship(back_populates="employee")

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    duration: Mapped[int] = mapped_column()
    description: Mapped[Optional[str]]
    employees: Mapped[List[Employee]] = relationship(
        back_populates="services", secondary="employee_services"
    )
    employee_associations: Mapped[List["EmployeeServices"]] = relationship(
         back_populates="service"
    )


    def __repr__(self) -> str:
        return f"Service(id={self.id!r}, title={self.title!r})"

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    employee: Mapped[Employee] = relationship(back_populates="bookings")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="bookings")
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    service: Mapped[Service] = relationship()
    notified: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime]

    @classmethod
    async def fetch_bookings(cls, date, user_id=None, employee_id=None):
        async with async_session_factory() as session:
            query = select(cls) \
                .filter(
                    (cls.user_id == user_id) | (cls.employee_id == employee_id),
                    func.DATE(cls.date) == date
                )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_booking(cls, employee_id, service_id, user_id, date):
        booking = cls(
            employee_id=employee_id,
            service_id=service_id,
            user_id=user_id,
            date=date
        )
        async with async_session_factory() as session:
            session.add(booking)
            await session.commit()
        return booking

    def __repr__(self) -> str:
        return f"Booking(employee={self.employee.firstname!r}, user={self.user.firstname!r}, service={self.service_id!r})"

class EmployeeServices(Base):
    __tablename__ = "employee_services"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), primary_key=True
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"), primary_key=True
    )
    employee: Mapped[Employee] = relationship(back_populates="service_associations")
    service: Mapped[Service] = relationship(back_populates="employee_associations")
    price: Mapped[float]

    def __repr__(self):
        return f"EmployeeServices(service_id={self.service_id!r}, employee_id={self.employee_id!r})"
