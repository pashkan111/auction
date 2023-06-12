import abc

from src.domains.users.schemas import user_schemas


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    async def create_user(self, bid_data: user_schemas.CreateUserInputSchema) -> user_schemas.UserSchema:
        ...

    @abc.abstractmethod
    async def get_user_by_username(self, username: str) -> user_schemas.UserSchema:
        ...
