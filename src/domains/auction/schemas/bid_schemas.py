import pydantic as pd

from src.utils.custom_data_types import PriceType


class CreateBidInputSchema(pd.BaseModel):
    amount: PriceType
    user_username: str
    auction_id: int

    class Config:
        allow_mutation = False

    @pd.validator('amount', pre=True)
    def validate_date(cls, value):
        return str(value)


class CreateBidOutputSchema(pd.BaseModel):
    bid_id: int
    current_price: PriceType


class BidSchema(pd.BaseModel):
    id: int
    auction_id: int
    user_username: str
    amount: PriceType

    class Config:
        orm_mode = True
        allow_mutation = False


class BidsSchema(pd.BaseModel):
    __root__: list[BidSchema]

    class Config:
        orm_mode = True


class GetBidsInputSchema(pd.BaseModel):
    limit: int | None = None
    offset: int | None = None
    user_username: str | None = None
    auction_id: int | None = None


class BidIdSchema(pd.BaseModel):
    bid_id: int


class UpdateBidSchema(pd.BaseModel):
    bid_id: int
    amount: PriceType | None = None

