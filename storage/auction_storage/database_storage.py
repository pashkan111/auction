from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import case, func
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

    async def get_auction_by_bid_id(self, bid_id: int) -> Auction | None:
        auction = await self.session.execute(
            sa.select(Auction)
            .join(Bid, Bid.auction_id == Auction.id)
            .where(Bid.id == bid_id)
        )
        return auction.scalar()

    async def get_current_price(self, auction_id: int) -> Decimal | None:
        case_expr = case(
            (func.max(Bid.amount).isnot(None), func.max(Bid.amount)),
            else_=Auction.start_price
        )
        query = (
            sa.select(case_expr)
            .select_from(Auction)
            .join(Bid, Auction.id == Bid.auction_id)
            .where(Auction.id == auction_id)
            .group_by(Auction.start_price)
        )
        price = await self.session.execute(query)
        return price.scalar()
