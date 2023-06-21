import abc
from collections.abc import Sequence

from src.domains.auction.models import Bid
from src.domains.auction.schemas import bid_schemas


class AbstractBidRepository(abc.ABC):
    @abc.abstractmethod
    async def create_bid(self, bid_data: bid_schemas.CreateBidInputSchema) -> Bid:
        ...

    @abc.abstractmethod
    async def get_bids(
        self,
        filter_params: bid_schemas.GetBidsInputSchema
    ) -> Sequence[Bid]:
        ...

    @abc.abstractmethod
    async def update_bid(self, update_data: bid_schemas.UpdateBidSchema) -> Bid:
        ...

    @abc.abstractmethod
    async def get_bid_by_id(self, bid_id: int) -> Bid:
        ...
