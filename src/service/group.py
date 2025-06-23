from typing import Any, Generic, TypeVar
from loguru import logger
import traceback

from ..interface import HTTPClient, ResponseLike
from ..shared.serializer import SerializerDTO
from ..model.group import DogGroupResponse, GroupDataItem, DogCurrentGroupResponse
from ..exception import (
    HttpStatusError,
    NetworkError,
    TimeoutError,
    HTTPError,
    RequestError,
)


T = TypeVar("T", bound=HTTPClient)


class GroupService(Generic[T]):
    """Service for working with dog groups."""

    def __init__(self, http_client: T) -> None:
        self._http_client: T = http_client

    def get_groups_by_page(self, page: int = 1) -> list[GroupDataItem]:
        """Get groups by page."""
        try:
            response: ResponseLike = self._http_client.get(
                "groups", params={"page[number]": page}
            )

        except HttpStatusError as e:
            if e.status_code == 404:
                logger.error(f"The page {page} does not exist.")
                return []

            if e.status_code != 200:
                logger.error(
                    f"Error getting groups by page {page}. Status code: {e.status_code}"
                )
                return []

        except RequestError as e:
            logger.error(f"Error getting groups by page {page}. {e.message}")
            return []

        except HTTPError as e:
            if isinstance(e, TimeoutError):
                logger.error(
                    f"Timeout error getting groups by page {page}. {e.message}"
                )

            if isinstance(e, NetworkError):
                logger.error(
                    f"Network error getting groups by page {page}. {e.message}"
                )

            else:
                tb_str = f"Error getting groups by page {page} " + "".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )
                logger.error(tb_str)

            return []

        try:
            data: dict[Any, Any] | list[Any] = response.json()

        except Exception as e:
            logger.error(
                f"Error getting groups by page {page}. {''.join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )}"
            )
            return []

        dto_response: DogGroupResponse = SerializerDTO(DogGroupResponse).serialize(data)

        result: list[GroupDataItem] = dto_response.data or []
        if page > 1 and not result:
            logger.warning("The maximum number of group pages has been exceeded.")
            return []

        return result

    def get_current_group(self, id: str) -> GroupDataItem | None:
        """Get group by id."""
        try:
            response: ResponseLike = self._http_client.get(f"groups/{id}")

        except HttpStatusError as e:
            if e.status_code != 200:
                logger.error(
                    f"Error getting group with id {id}. Status code: {e.status_code}"
                )
                return None

        except RequestError as e:
            logger.error(f"Error getting group with id {id}. {e.message}")
            return None

        except HTTPError as e:
            if isinstance(e, TimeoutError):
                logger.error(f"Timeout error getting group with id {id}. {e.message}")

            if isinstance(e, NetworkError):
                logger.error(f"Network error getting group with id {id}. {e.message}")

            else:
                tb_str = "".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )
                logger.error(tb_str)

            return None

        try:
            data: dict[Any, Any] | list[Any] = response.json()

        except Exception as e:
            logger.error(
                f"Error getting group with id {id}. {''.join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )}"
            )
            return None

        dto_response: DogCurrentGroupResponse = SerializerDTO(
            DogCurrentGroupResponse
        ).serialize(data)

        result: GroupDataItem | None = dto_response.data
        if not result:
            logger.error(f"The group with id {id} does not exist.")
            return None

        return result
