from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.domains.auction.containers import UseCaseContainer
from src.domains.auction.schemas.bid_schemas import (CreateBidInputSchema,
                                                     CreateBidOutputSchema,
                                                     GetBidsInputSchema)
from src.domains.auction.use_cases import bid_use_cases
from src.utils.api_result_decorator import result_decorator
from storage.db_config import AsyncSession, get_session

bid_router = APIRouter(prefix='/bids', tags=['bids'])


@bid_router.post('/', response_model=CreateBidOutputSchema)
@result_decorator
@inject
async def create_bid(
    data: CreateBidInputSchema,
    use_case: bid_use_cases.CreateBidUseCase = Depends(Provide[UseCaseContainer.create_bid_use_case]),
):
    result = await use_case.execute(data)
    return result


@bid_router.get('/')
@result_decorator
@inject
async def get_bids(
    query_params: GetBidsInputSchema = Depends(),
    use_case: bid_use_cases.GetBidsUseCase = Depends(Provide[UseCaseContainer.get_bids_use_case])
):
    result = await use_case.execute(query_params)
    return result
