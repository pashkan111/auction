from src.domains.auction.schemas.bid_schemas import (BidsSchema,
                                                     CreateBidOutputSchema)
from src.utils.abstract_presenter import AbstractPresenter


class CreateBidPresenter(AbstractPresenter):
    def present(self, model):
        return CreateBidOutputSchema(bid_id=model.id, current_price=model.amount)


class GetBidsPresenter(AbstractPresenter):
    def present(self, models):
        return BidsSchema.from_orm(models)
