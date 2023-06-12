import abc

from src.domains.auction.models import Auction
from src.domains.auction.schemas import auction_schemas


class AbstractAuctionRepository(abc.ABC):
    @abc.abstractmethod
    async def create_auction(self, bid_data: auction_schemas.CreateAuctionInputSchema) -> Auction:
        ...

    @abc.abstractmethod
    async def get_auction_by_id(self, auction_id: int) -> Auction:
        ...
