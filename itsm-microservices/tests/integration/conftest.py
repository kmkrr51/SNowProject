import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.shared.infrastructure import Base


@pytest.fixture(scope="session")
def event_loop():
  loop = asyncio.get_event_loop_policy().new_event_loop()
  yield loop
  loop.close()


@pytest.fixture(scope="session")
async def engine():
  engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  yield engine
  await engine.dispose()


@pytest.fixture
async def session(engine):
  async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
  async with async_session() as session:
    yield session
    await session.rollback()
