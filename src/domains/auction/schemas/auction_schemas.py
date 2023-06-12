from decimal import Decimal

import pydantic as pd


class CreateAuctionInputSchema(pd.BaseModel):
    current_price: Decimal


class AuctionSchema(pd.BaseModel):
    id: int
    current_price: Decimal

    class Config:
        orm_mode = True
