from abc import ABCMeta, abstractmethod


class HTTPClient(metaclass=ABCMeta):
    @abstractmethod
    def get(self, endpoint: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def post(self, endpoint: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def put(self, endpoint: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, endpoint: str, **kwargs):
        raise NotImplementedError
