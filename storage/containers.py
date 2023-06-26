from dependency_injector import containers, providers

from storage.auction_storage import database_storage as auction_storage
from storage.bid_storage import database_storage as bid_storage
from storage.db_config import Session
from storage.storage_session import StorageSessionContext
from storage.user_storage import database_storage as user_storage


class RepositoryContainer(containers.DeclarativeContainer):
    session = providers.Factory(Session)

    auction_repo = providers.Singleton(
        auction_storage.DatabaseAuctionRepository,
        session=session
    )
    bid_repo = providers.Singleton(
        bid_storage.DatabaseBidStorage,
        session=session
    )
    user_repo = providers.Singleton(
        user_storage.DatabaseUserStorage,
        session=session
    )

    session_storage = providers.Singleton(
        StorageSessionContext,
        auction_repository=auction_repo,
        bid_repository=bid_repo,
        user_repository=user_repo,
        session=session
    )
