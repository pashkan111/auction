from dependency_injector import containers, providers

from src.domains.auction.presenters import presenters
from src.domains.auction.use_cases import bid_use_cases
from storage.containers import RepositoryContainer


class UseCaseContainer(containers.DeclarativeContainer):
    repositories = providers.Container(RepositoryContainer)
    session_storage = providers.Dependency()

    create_bid_presenter = providers.Singleton(presenters.CreateBidPresenter)
    create_bid_use_case = providers.Factory(
        bid_use_cases.CreateBidUseCase,
        presenter=create_bid_presenter,
        storage_context=repositories.session_storage
    )

    get_bids_presenter = providers.Singleton(presenters.GetBidsPresenter)
    get_bids_use_case = providers.Factory(
        bid_use_cases.GetBidsUseCase,
        presenter=get_bids_presenter,
        storage_context=repositories.session_storage
    )
