from abc import ABC, abstractmethod
from typing import Any, Protocol


class ResponseLike(Protocol):
    def json(self) -> dict[Any, Any] | list[Any]:
        raise NotImplementedError


class HTTPClient(ABC):
    @abstractmethod
    def get(
        self,
        endpoint: str,
        params: dict[Any, Any] | None = None,
        **kwargs: dict[str, Any]
    ) -> ResponseLike:
        raise NotImplementedError
