import abc

from pydantic import BaseModel

from src.domains.auction.presenters.abstract_presenter import AbstractPresenter
from src.domains.auction.schemas import bid_schemas
from src.domains.auction.services.auction import validate_bid
from src.exceptions.auction_exceptions import AuctionDoesNotExists
from src.exceptions.exceptions import StorageException
from src.exceptions.user_exceptions import UserDoesNotExists
from storage.storage_session import AbstractStorageSessionContext


class AbstractBidUseCase(abc.ABC):
    def __init__(
        self,
        storage_context: AbstractStorageSessionContext,
        presenter: AbstractPresenter
    ):
        self.storage_context = storage_context
        self.presenter = presenter

    @abc.abstractmethod
    async def execute(self, bid_data: BaseModel):
        pass


class CreateBidUseCase(AbstractBidUseCase):
    async def execute(self, bid_data: bid_schemas.CreateBidInputSchema):
        async with self.storage_context as storage:

            auction = await self.storage_context.auction_repository.get_auction_by_id(bid_data.auction_id)
            if auction is None:
                raise AuctionDoesNotExists

            validate_bid(auction, bid_data.amount)

            user = await self.storage_context.user_repository.get_user_by_username(bid_data.user_username)
            if user is None:
                raise UserDoesNotExists

            try:
                bid = await storage.bid_repository.create_bid(bid_data)
            except Exception as e:
                print(e)
                # TODO add logging
                raise StorageException
        return self.presenter.present(bid)


class GetBidsUseCase(AbstractBidUseCase):
    async def execute(self, filter_params: bid_schemas.GetBidsInputSchema):
        async with self.storage_context as storage:
            bids = await storage.bid_repository.get_bids(filter_params)
        return self.presenter.present(bids)
