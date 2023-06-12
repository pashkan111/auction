import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from config import settings
from storage.auction_storage.database_storage import DatabaseAuctionRepository
from storage.bid_storage.database_storage import DatabaseBidStorage
from storage.storage_session import StorageSessionContext
from storage.user_storage.database_storage import DatabaseUserStorage

postgres_url = (
    f"postgresql+asyncpg://{settings.TEST_POSTGRES_USER}:{settings.TEST_POSTGRES_PASSWORD}@"
    f"{settings.TEST_POSTGRES_HOST}:{settings.TEST_POSTGRES_PORT}/{settings.TEST_POSTGRES_DB}"
)

async_engine = create_async_engine(
   postgres_url,
   echo=True,
   future=True
)

db_session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=async_engine,
        class_=AsyncSession,
    ),
    scopefunc=asyncio.current_task,
)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_session() as session:
        async with async_engine.begin() as conn:
            from src.domains.auction.models import Base
            from src.domains.users.models import Base
            await conn.run_sync(Base.metadata.create_all)
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest.fixture(scope="function")
def storage_session(async_session):
    auction_storage = DatabaseAuctionRepository(async_session)
    bid_storage = DatabaseBidStorage(async_session)
    user_storage = DatabaseUserStorage(async_session)
    return StorageSessionContext(
        async_session,
        auction_storage,
        bid_storage,
        user_storage
    )
