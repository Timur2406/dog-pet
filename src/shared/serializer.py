from typing import Any, Generic, ParamSpec, TypeVar
from pydantic import BaseModel

from src.exception.serialization import SerializationError

T = TypeVar("T", bound=BaseModel)

P = ParamSpec("P")


class SerializerDTO(Generic[T]):
    def __init__(self, _to: type[T]) -> None:
        self._to: type[T] = _to

    def serialize(self, _from: dict[Any, Any] | list[Any]) -> T:
        if isinstance(_from, list):
            raise SerializationError("List serialization not supported", _from)
        return self._to.model_validate(_from, from_attributes=True)
