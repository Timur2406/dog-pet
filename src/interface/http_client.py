from abc import ABC, abstractmethod
from typing import Any, Protocol


class ResponseLike(Protocol):
    def json(self) -> dict | list:
        raise NotImplementedError


class HTTPClient(ABC):
    @abstractmethod
    def get(
        self, endpoint: str, params: dict | None = None, **kwargs: dict[str, Any]
    ) -> ResponseLike:
        raise NotImplementedError
