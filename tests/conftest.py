import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.database import Base

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=True
)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(autouse=True)
async def mock_factory(mocker):
    mocker.patch("core.database.async_session_factory", return_value=async_session_factory())
    mocker.patch("core.models.async_session_factory", return_value=async_session_factory())
    mocker.patch("core.utils.async_session_factory", return_value=async_session_factory())

@pytest_asyncio.fixture(autouse=True)
async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def session():
    session = async_session_factory()
    try:
        yield session
    except Exception as e:
        print (str(e))
    finally:
        await session.close()


