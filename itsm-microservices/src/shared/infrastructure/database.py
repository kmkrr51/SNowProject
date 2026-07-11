from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

Base = declarative_base()


async def get_database_engine():
  engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
  )
  return engine


async def get_session_factory(engine):
  return async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_fetch=False,
    autocommit=False,
    autoflush=False,
  )


async def init_db(engine):
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)


async def close_db(engine):
  await engine.dispose()
