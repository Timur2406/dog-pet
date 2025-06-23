from typing import Any, Generic, TypeVar
from loguru import logger
import traceback

from ..interface import HTTPClient, ResponseLike
from ..shared.serializer import SerializerDTO
from ..model.fact import DogFactResponse, FactDataItem
from ..exception import (
    HttpStatusError,
    NetworkError,
    TimeoutError,
    HTTPError,
    RequestError,
)


T = TypeVar("T", bound=HTTPClient)


class FactService(Generic[T]):
    """Service for working with dog facts."""

    def __init__(self, http_client: T) -> None:
        self._http_client: T = http_client

    def get_facts(
        self,
        limit: int = 10,
    ) -> list[FactDataItem]:
        """Get facts."""
        try:
            response: ResponseLike = self._http_client.get(
                "facts", params={"limit": limit}
            )

        except HttpStatusError as e:
            if e.status_code == 404:
                logger.error("The facts page does not exist.")
                return []

            if e.status_code != 200:
                logger.error(f"Error getting facts. Status code: {e.status_code}")
                return []

        except RequestError as e:
            logger.error(f"Error getting facts. {e.message}")
            return []

        except HTTPError as e:
            if isinstance(e, TimeoutError):
                logger.error(f"Timeout error getting facts. {e.message}")

            if isinstance(e, NetworkError):
                logger.error(f"Network error getting facts. {e.message}")

            else:
                tb_str = "Error getting facts. " + "".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )
                logger.error(tb_str)

            return []

        try:
            data: dict[Any, Any] | list[Any] = response.json()

        except Exception as e:
            logger.error(
                f"Error getting facts. {''.join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )}"
            )
            return []

        dto_response: DogFactResponse = SerializerDTO(DogFactResponse).serialize(data)
        result: list[FactDataItem] = dto_response.data or []

        return result
