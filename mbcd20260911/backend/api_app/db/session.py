"""Асинхронная сессия SQLAlchemy для FastAPI (dependency get_session)."""
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api_app.core.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
