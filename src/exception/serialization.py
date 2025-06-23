from typing import Any


class SerializationError(Exception):
    """Serialization error."""

    def __init__(self, message: str, data: Any) -> None:
        super().__init__(message)
        self.data = data
