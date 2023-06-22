import abc


class AbstractPresenter(abc.ABC):

    @abc.abstractmethod
    def present(self, model):
        ...
