import abc


class AbstractPresenter(abc.ABC):

    @abc.abstractmethod
    def present(self, model):
        ...

    @abc.abstractmethod
    def get_presented_data(self):
        ...
