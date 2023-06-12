import datetime

import pydantic as pd


class CreateUserInputSchema(pd.BaseModel):
    username: str
    password: str


class UserSchema(CreateUserInputSchema):
    created: datetime.datetime

    class Config:
        orm_mode = True
