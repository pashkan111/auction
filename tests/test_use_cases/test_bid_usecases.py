from decimal import Decimal

import pytest
from faker import Faker
from pydantic import ValidationError

from src.domains.auction.presenters.presenters import (CreateBidPresenter,
                                                       GetBidsPresenter)
from src.domains.auction.schemas.auction_schemas import \
    CreateAuctionInputSchema
from src.domains.auction.schemas.bid_schemas import (CreateBidInputSchema,
                                                     GetBidsInputSchema)
from src.domains.auction.use_cases.bid_use_cases import (CreateBidUseCase,
                                                         GetBidsUseCase)
from src.domains.users.schemas.user_schemas import CreateUserInputSchema
from src.exceptions.exceptions import (DoesNotExistsException,
                                       InvalidDataException)


@pytest.mark.asyncio
async def test_error_create_bid(storage_session):
    bid_presenter = CreateBidPresenter()
    bid_use_case = CreateBidUseCase(storage_session, bid_presenter)
    data = CreateBidInputSchema(
        amount=Decimal('100.00'),
        user_username='user1',
        auction_id=1
    )
    with pytest.raises(DoesNotExistsException):
        await bid_use_case.execute(data)


@pytest.mark.asyncio
async def test_create_bid(storage_session):
    bid_presenter = CreateBidPresenter()
    async with storage_session as storage:

        user = await storage.user_repository.create_user(
            CreateUserInputSchema(username='user1', password='123')
        )
        auction = await storage.auction_repository.create_auction(
            CreateAuctionInputSchema(current_price=Decimal('100.00'))
        )
    bid_use_case = CreateBidUseCase(storage_session, bid_presenter)
    data = CreateBidInputSchema(
        amount=Decimal('100.00'),
        user_username=user.username,
        auction_id=auction.id
    )
    result = await bid_use_case.execute(data)
    assert result.bid_id is not None
    assert result.current_price == data.amount


@pytest.mark.asyncio
async def test_create_bid_with_lower_amount(storage_session):
    bid_presenter = CreateBidPresenter()
    async with storage_session as storage:
        user = await storage.user_repository.create_user(
            CreateUserInputSchema(username='user1', password='123')
        )
        auction = await storage.auction_repository.create_auction(
            CreateAuctionInputSchema(current_price=Decimal('100.00'))
        )
    bid_use_case = CreateBidUseCase(storage_session, bid_presenter)
    data = CreateBidInputSchema(
        amount=Decimal('99.00'),
        user_username=user.username,
        auction_id=auction.id
    )
    with pytest.raises(InvalidDataException):
        await bid_use_case.execute(data)


@pytest.mark.asyncio
async def test_get_bids(storage_session):
    bid_presenter = GetBidsPresenter()
    async with storage_session as storage:
        user = await storage.user_repository.create_user(
            CreateUserInputSchema(username='user1', password='123')
        )
        auction = await storage.auction_repository.create_auction(
            CreateAuctionInputSchema(current_price=Decimal('100.00'))
        )
        await storage.bid_repository.create_bid(
            CreateBidInputSchema(
                amount=Decimal('101.00'),
                user_username=user.username,
                auction_id=auction.id
            )
        )
        await storage.bid_repository.create_bid(
            CreateBidInputSchema(
                amount=Decimal('102.00'),
                user_username=user.username,
                auction_id=auction.id
            )
        )
    bid_use_case = GetBidsUseCase(storage_session, bid_presenter)
    data = GetBidsInputSchema()
    result = await bid_use_case.execute(data)
    assert len(result.__root__) == 2


@pytest.mark.parametrize(['amount'], [
    (Decimal('0.01'),),
    (Decimal('12.38'),),
    (Decimal('1'),),
    (Decimal('0.01'),)
])
def test_PriceType(amount, faker: Faker):
    CreateBidInputSchema(
        amount=amount,
        user_username=faker.name(),
        auction_id=faker.pyint()
    )


@pytest.mark.parametrize(['amount'], [
    (Decimal('0'),),
    (Decimal('-2.77'),)
])
def test_fail_PriceType(amount, faker: Faker):
    with pytest.raises(ValidationError):
        CreateBidInputSchema(
            amount=amount,
            user_username=faker.name(),
            auction_id=faker.pyint()
        )


def test_mutation_class(faker):
    schema = CreateBidInputSchema(
        amount=Decimal('1.99'),
        user_username=faker.name(),
        auction_id=faker.pyint()
    )
    with pytest.raises(TypeError):
        schema.auction_id = 10
