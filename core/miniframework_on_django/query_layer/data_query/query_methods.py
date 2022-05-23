from abc import ABCMeta, abstractmethod


class QueryMethod(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class QueryReader(QueryMethod, metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class QueryCreator(QueryMethod, metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class QueryUpdator(QueryMethod, metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class QueryDestroyer(QueryMethod, metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class QuerySearcher(QueryMethod, metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
