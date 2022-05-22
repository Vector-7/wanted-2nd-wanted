from abc import ABCMeta


class BaseManagerLayer(metaclass=ABCMeta):
    pass


class FrontendManagerLayer(BaseManagerLayer, metaclass=ABCMeta):
    pass


class BackendManagerLayer(BaseManagerLayer, metaclass=ABCMeta):
    pass
