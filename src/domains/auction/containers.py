from dependency_injector import containers, providers

from src.containers import RepositoryContainer
from src.domains.auction.presenters import presenters
from src.domains.auction.use_cases import bid_use_cases


class UseCaseContainer(containers.DeclarativeContainer):
    repositories = providers.Container(RepositoryContainer)

    presenter = providers.Singleton(presenters.CreateBidPresenter)
    session_storage = providers.Dependency()
    create_bid_use_case = providers.Factory(
        bid_use_cases.CreateBidUseCase,
        presenter=presenter,
        storage_context=repositories.session_storage
    )
