import abc

from pydantic import BaseModel

from storage.storage_session import AbstractStorageSessionContext

from .abstract_presenter import AbstractPresenter


class AbstractUseCase(abc.ABC):
    def __init__(
        self,
        storage_context: AbstractStorageSessionContext,
        presenter: AbstractPresenter
    ):
        self.storage_context = storage_context
        self.presenter = presenter

    @abc.abstractmethod
    async def execute(self, data: BaseModel):
        pass
