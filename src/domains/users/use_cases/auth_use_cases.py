from src.domains.users.schemas.user_schemas import CreateUserInputSchema
from src.utils.abstract_use_case import AbstractUseCase


class CreateUserUseCase(AbstractUseCase):
    async def execute(self, data: CreateUserInputSchema):
        async with self.storage_context as storage:
            user = await storage.user_repository.create_user(data)
            return self.presenter.present(user)
