from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

Base = declarative_base()

postgres_url = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

async_engine = create_async_engine(
    postgres_url,
    pool_size=10,
    echo=True,
)


async def init_db():
    from src.domains.auction.models import Base
    from src.domains.users.models import Base
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


Session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=async_engine,
        class_=AsyncSession,
    ),
    scopefunc=current_task,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
