from dependency_injector import containers, providers

import storage


class RepositoryContainer(containers.DeclarativeContainer):
    session = providers.Singleton(storage.Session)

    auction_repo = providers.Singleton(
        storage.DatabaseAuctionRepository,
        session=session
    )
    bid_repo = providers.Singleton(
        storage.DatabaseBidStorage,
        session=session
    )
    user_repo = providers.Singleton(
        storage.DatabaseUserStorage,
        session=session
    )

    session_storage = providers.Singleton(
        storage.StorageSessionContext,
        auction_repository=auction_repo,
        bid_repository=bid_repo,
        user_repository=user_repo,
        session=session
    )
