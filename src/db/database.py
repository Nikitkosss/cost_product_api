from typing import Any
from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, poolclass=NullPool)

SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, class_=AsyncSession, bind=engine
)

sync_engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"),
    echo=False,
    poolclass=NullPool,
)

Base: Any = declarative_base()


def create_tables_sync():
    Base.metadata.create_all(bind=sync_engine)
