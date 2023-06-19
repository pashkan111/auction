import pytest

from src.domains.users.presenters.presenters import CreateUserPresenter
from src.domains.users.schemas.user_schemas import CreateUserInputSchema
from src.domains.users.services.auth import get_password_hash
from src.domains.users.use_cases.auth_use_cases import CreateUserUseCase


# from src.domains.users.
@pytest.mark.asyncio
async def test_create_user(storage_session):
    user_presenter = CreateUserPresenter()
    password = 'password12'
    username = 'username1'
    user_data = CreateUserInputSchema(username=username, password=password)
    create_user_use_case = CreateUserUseCase(storage_session, user_presenter)
    user = await create_user_use_case.execute(user_data)
    assert user.password == get_password_hash(password)
    assert user.username == username
    assert user.created is not None
