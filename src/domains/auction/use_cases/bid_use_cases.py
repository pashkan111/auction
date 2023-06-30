from src.domains.auction.schemas import bid_schemas
from src.domains.auction.services.auction import validate_bid
from src.exceptions.auction_exceptions import (AuctionDoesNotExists,
                                               BidDoesNotExists)
from src.exceptions.exceptions import StorageException
from src.exceptions.user_exceptions import UserDoesNotExists
from src.utils.abstract_use_case import AbstractUseCase


class CreateBidUseCase(AbstractUseCase):
    async def execute(self, bid_data: bid_schemas.CreateBidInputSchema):
        async with self.storage_context as storage:

            auction = await self.storage_context.auction_repository.get_auction_by_id(bid_data.auction_id)
            if auction is None:
                raise AuctionDoesNotExists

            auction_current_price = await self.storage_context.auction_repository.get_current_price(auction.id)
            validate_bid(auction_current_price, bid_data.amount)

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


class GetBidsUseCase(AbstractUseCase):
    async def execute(self, filter_params: bid_schemas.GetBidsInputSchema):
        async with self.storage_context as storage:
            bids = await storage.bid_repository.get_bids(filter_params)
        return self.presenter.present(bids)


class SetBidWinnerUseCase(AbstractUseCase):
    async def execute(self, data: bid_schemas.UpdateBidSchema):
        async with self.storage_context as storage:
            bid = await storage.bid_repository.get_bid_by_id(data.bid_id)
            if bid is None:
                raise BidDoesNotExists
            
            auction = await storage.auction_repository.get_auction_by_bid_id(data.bid_id)
            validate_bid(auction, data.amount)

            bid = await storage.bid_repository.update_bid(data)
