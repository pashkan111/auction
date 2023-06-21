from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.auction.models import Bid
from src.domains.auction.schemas import bid_schemas

from .abstract_bid_storage import AbstractBidRepository


class DatabaseBidStorage(AbstractBidRepository):
    batch_size = 10

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_bid(self, bid_data: bid_schemas.CreateBidInputSchema) -> Bid:
        bid = await self.session.execute(
            sa.insert(Bid)
            .returning(Bid)
            .values(**bid_data.dict())
        )
        return bid.scalar()

    async def get_bids(
        self,
        filter_params: bid_schemas.GetBidsInputSchema
    ) -> Sequence[Bid]:
        query = sa.select(Bid)
        if filter_params.user_username is not None:
            query = query.where(Bid.user_username == filter_params.user_username)
        if filter_params.auction_id is not None:
            query = query.where(Bid.auction_id == filter_params.auction_id)
        if filter_params.limit is not None:
            query = query.limit(filter_params.limit)
        if filter_params.offset is not None:
            query = query.offset(filter_params.offset)
        bids_executed = await self.session.execute(query)
        bids = bids_executed.scalars().fetchall()
        return bids

    async def update_bid(self, update_data: bid_schemas.UpdateBidSchema) -> Bid:
        bid = await self.session.execute(
            sa.update(Bid)
            .returning(Bid)
            .values(**update_data.dict(exclude={'bid_id'}))
            .where(Bid.id == update_data.bid_id)
        )
        return bid.scalar()

    async def get_bid_by_id(self, bid_id: int) -> Bid:
        bid = await self.session.execute(
            sa.select(Bid)
            .where(Bid.id == bid_id)
        )
        return bid.scalar()
