import abc
from typing import NoReturn

from src.domains.users.models import User
from src.domains.users.schemas import user_schemas


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    async def create_user(self, bid_data: user_schemas.CreateUserInputSchema) -> User:
        ...

    @abc.abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        ...

    @abc.abstractmethod
    async def authenticate_user(self, auth_data: user_schemas.AuthUserSchema) -> User | NoReturn:
        ...
