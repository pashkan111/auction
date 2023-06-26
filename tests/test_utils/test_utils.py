import pytest
from faker import Faker
from pydantic import ValidationError

from src.domains.auction.schemas import bid_schemas
from src.domains.auction.schemas.bid_schemas import CreateBidInputSchema
from src.utils.custom_data_types import PriceType


@pytest.mark.parametrize(['amount'], [
    (PriceType('0.01'),),
    (PriceType('12.38'),),
    (PriceType('1'),),
    (PriceType('0.01'),)
])
def test_PriceType(amount, faker: Faker):
    bid_schemas.CreateBidInputSchema(
        amount=amount,
        user_username=faker.name(),
        auction_id=faker.pyint()
    )


@pytest.mark.parametrize(['amount'], [
    (PriceType('0'),),
    (PriceType('-2.77'),)
])
def test_fail_PriceType(amount, faker: Faker):
    with pytest.raises(ValidationError):
        bid_schemas.CreateBidInputSchema(
            amount=amount,
            user_username=faker.name(),
            auction_id=faker.pyint()
        )


def test_mutation_class(faker):
    schema = bid_schemas.CreateBidInputSchema(
        amount=PriceType('1.99'),
        user_username=faker.name(),
        auction_id=faker.pyint()
    )
    with pytest.raises(TypeError):
        schema.auction_id = 10


@pytest.mark.asyncio
async def test_auction_current_price(auction, storage_session, user):
    bid1_amount = PriceType('101.00')
    bid2_amount = PriceType('270.00')
    async with storage_session as storage:
        await storage.bid_repository.create_bid(
            CreateBidInputSchema(
                amount=bid1_amount,
                user_username=user.username,
                auction_id=auction.id
            )
        )
        await storage.bid_repository.create_bid(
            CreateBidInputSchema(
                amount=bid2_amount,
                user_username=user.username,
                auction_id=auction.id
            )
        )

    async with storage_session as storage:
        auction_current_price = await storage.auction_repository.get_current_price(auction.id)
        assert auction_current_price == bid2_amount
