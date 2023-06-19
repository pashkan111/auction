import pydantic as pd

from src.utils.custom_data_types import PriceType


class CreateAuctionInputSchema(pd.BaseModel):
    current_price: PriceType


class AuctionSchema(pd.BaseModel):
    id: int
    current_price: PriceType

    class Config:
        orm_mode = True
