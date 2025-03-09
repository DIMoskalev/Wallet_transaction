import os
import pytest

os.environ['TEST'] = 'True'

from typing import AsyncGenerator
import asyncio

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.config import get_test_db_url
from app.database import get_db, Base
from app.main import app as application

# DATABASE
DATABASE_URL_TEST = get_test_db_url()

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


application.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(application)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=application), base_url="http://test", ) as ac:
        yield ac
