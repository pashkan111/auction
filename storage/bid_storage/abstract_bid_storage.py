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
