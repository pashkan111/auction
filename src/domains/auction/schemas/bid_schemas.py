from decimal import Decimal

import pydantic as pd


class CreateBidInputSchema(pd.BaseModel):
    amount: Decimal
    user_username: str
    auction_id: int


class CreateBidOutputSchema(pd.BaseModel):
    bid_id: int
    current_price: Decimal


class BidSchema(pd.BaseModel):
    id: int
    auction_id: int
    user_username: str
    amount: Decimal

    class Config:
        orm_mode = True


class BidsSchema(pd.BaseModel):
    __root__: list[BidSchema]

    class Config:
        orm_mode = True


class GetBidsInputSchema(pd.BaseModel):
    limit: int | None = None
    offset: int | None = None
    user_username: str | None = None
    auction_id: int | None = None
