from src.domains.users.models import User
from src.domains.users.schemas.user_schemas import UserSchema
from src.utils.abstract_presenter import AbstractPresenter


class CreateUserPresenter(AbstractPresenter):
    def present(self, model: User) -> UserSchema:
        return UserSchema.from_orm(model)
