import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.users.models import User
from src.domains.users.schemas import user_schemas

from .abstract_user_storage import AbstractUserRepository


class DatabaseUserStorage(AbstractUserRepository):
    batch_size = 100

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: user_schemas.CreateUserInputSchema) -> User:
        user = await self.session.execute(
            sa.insert(User)
            .returning(User)
            .values(**user_data.dict())
        )
        return user.scalar()

    async def get_user_by_username(self, username: str) -> User:
        query = (
            sa.select(User)
            .where(User.username == username)
        )
        user_executed = await self.session.execute(query)
        user = user_executed.scalar()
        return user
