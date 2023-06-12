import abc
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from storage.auction_storage.abstract_auction_storage import \
    AbstractAuctionRepository
from storage.auction_storage.database_storage import DatabaseAuctionRepository
from storage.bid_storage.abstract_bid_storage import AbstractBidRepository
from storage.bid_storage.database_storage import DatabaseBidStorage
from storage.db_config import get_session
from storage.user_storage.abstract_user_storage import AbstractUserRepository
from storage.user_storage.database_storage import DatabaseUserStorage


class AbstractStorageSessionContext(abc.ABC):
    auction_repository: AbstractAuctionRepository
    bid_repository: AbstractBidRepository
    user_repository: AbstractUserRepository

    @abc.abstractmethod
    async def __aenter__(self) -> "AbstractStorageSessionContext":
        ...

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...


class StorageSessionContext(AbstractStorageSessionContext):
    def __init__(
        self,
        session: AsyncSession,
        auction_repository: AbstractAuctionRepository,
        bid_repository: AbstractBidRepository,
        user_repository: AbstractUserRepository,
    ):
        self.auction_repository = auction_repository
        self.bid_repository = bid_repository
        self.user_repository = user_repository
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


def get_storage_session_context(
    session: AsyncSession = Depends(get_session),
) -> StorageSessionContext:
    auction_repository = DatabaseAuctionRepository(session)
    bid_repository = DatabaseBidStorage(session)
    user_repository = DatabaseUserStorage(session)

    return StorageSessionContext(
        session,
        auction_repository,
        bid_repository,
        user_repository,
    )
