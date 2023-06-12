from fastapi import APIRouter, Depends

from src.domains.auction.presenters.presenters import (AbstractPresenter,
                                                       CreateBidPresenter,
                                                       GetBidsPresenter)
from src.domains.auction.schemas.bid_schemas import (CreateBidInputSchema,
                                                     CreateBidOutputSchema,
                                                     GetBidsInputSchema)
from src.domains.auction.use_cases import bid_use_cases
from src.utils.api_result_decorator import result_decorator
from storage.storage_session import (StorageSessionContext,
                                     get_storage_session_context)

bid_router = APIRouter(prefix='/bids', tags=['bids'])


@bid_router.post('/', response_model=CreateBidOutputSchema)
@result_decorator
async def create_bid(
    data: CreateBidInputSchema,
    storage_context: StorageSessionContext = Depends(get_storage_session_context),
):
    presenter: AbstractPresenter = CreateBidPresenter()
    use_case = bid_use_cases.CreateBidUseCase(storage_context, presenter)
    result = await use_case.execute(data)
    return result


@bid_router.get('/')
@result_decorator
async def get_bids(
    query_params: GetBidsInputSchema = Depends(),
    storage_context: StorageSessionContext = Depends(get_storage_session_context)
):
    presenter: AbstractPresenter = GetBidsPresenter()
    use_case = bid_use_cases.GetBidsUseCase(storage_context, presenter)
    result = await use_case.execute(query_params)
    return result
