from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import Settings

DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:5432/{}?async_fallback=True".format(
    Settings.POSTGRES_USER,
    Settings.POSTGRES_PASSWORD,
    Settings.POSTGRES_HOST,
    Settings.POSTGRES_DB
)

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
