from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.auction.models import Auction, Bid
from src.domains.auction.schemas import auction_schemas

from .abstract_auction_storage import AbstractAuctionRepository


class DatabaseAuctionRepository(AbstractAuctionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_auction(self, auction_data: auction_schemas.CreateAuctionInputSchema) -> Auction:
        auction = await self.session.execute(
            sa.insert(Auction)
            .returning(Auction)
            .values(**auction_data.dict())
        )
        return auction.scalar()

    async def get_auction_by_id(self, auction_id: int) -> auction_schemas.AuctionSchema:
        auction = await self.session.get(Auction, auction_id)
        return auction
