import asyncio
from src.shared.infrastructure import get_database_engine
from src.shared.infrastructure.database import Base

async def clear_database():
  engine = await get_database_engine()
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
    await conn.run_sync(Base.metadata.create_all)
  await engine.dispose()
  print("Database cleared and recreated successfully!")

if __name__ == "__main__":
  asyncio.run(clear_database())
