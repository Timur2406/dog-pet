from collections.abc import Callable, Iterable, Sequence
from typing import Generic, ParamSpec, TypeAlias, TypeVar, overload

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
_T = TypeVar("_T")
RT = TypeVar("RT")
RTA: TypeAlias = _T | Iterable[_T]

P = ParamSpec("P")


class SerializerDTO(Generic[T, RT]):
    def __init__(self, _to: type[T]) -> None:
        self._to: type[T] = _to

    @overload
    def serialize(self, _from: RT) -> T: ...
    @overload
    def serialize(self, _from: Iterable[RT]) -> Sequence[T]: ...

    def serialize(self, _from: RT | Iterable[RT]) -> T | Sequence[T]:
        return self._to.model_validate(_from, from_attributes=True)

    @overload
    def __call__(self, func: Callable[P, RT]) -> Callable[P, T]: ...

    @overload
    def __call__(self, func: Callable[P, Iterable[RT]]) -> Callable[P, Sequence[T]]: ...

    def __call__(
        self, func: Callable[P, RT | Iterable[RT]]
    ) -> Callable[P, T | Sequence[T]]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | Sequence[T]:
            result: RTA[RT] = func(*args, **kwargs)
            return self.serialize(result)

        return wrapper
