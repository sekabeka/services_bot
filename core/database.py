from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from sqlalchemy.orm import DeclarativeBase, joinedload
from sqlalchemy import select
from settings import SALON_ID, DATABASE_URL

mappings = {
    "Employee": lambda cls: (joinedload(cls.services)),
    "Service": lambda cls: (
        joinedload(cls.employees),
        joinedload(cls.employee_associations)
    )
}

async_engine = create_async_engine(
    DATABASE_URL, echo=True
)

async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=True
)

class Base(DeclarativeBase):
    @classmethod
    async def all(cls):
        async with async_session_factory() as session:
            stmt, options = select(cls), None
            if cls.__name__ in mappings:
                options = mappings[cls.__name__](cls)
                stmt = stmt.options(*options).filter(cls.salon == SALON_ID)

            result = await session.execute(stmt)
            if options:
                return result.unique().scalars().all()

            return result.scalars().all()

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        async with async_session_factory() as session:
            session.add(obj)
            await session.commit()
        return obj

    async def update_fields(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

async def init_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


