from typing import Generic, TypeVar
from loguru import logger
import traceback

from ..interface import HTTPClient, ResponseLike
from ..shared.serializer import SerializerDTO
from ..model.breed import DogBreedResponse, BreedDataItem, DogCurrentBreedResponse
from ..exception import (
    HttpStatusError,
    NetworkError,
    TimeoutError,
    HTTPError,
    RequestError,
)


T = TypeVar("T", bound=HTTPClient)


class BreedService(Generic[T]):
    def __init__(self, http_client: type[T]) -> None:
        self._http_client: type[T] = http_client
        self._records_count: int | None = None

    @property
    def records_count(self) -> int:
        if self._records_count is None:
            self.get_breeds_by_page()
        if self._records_count is None:
            raise RuntimeError("Records count was not loaded correctly")
        return self._records_count

    @property
    def records_page_count(self) -> int:
        return self.records_count // 10 + 1

    def get_breeds_by_page(self, page: int = 1) -> list[BreedDataItem]:
        try:
            response: ResponseLike = self._http_client.get(
                "breeds", params={"page[number]": page}
            )

        except HttpStatusError as e:
            if e.status_code == 404:
                logger.error(f"The page {page} does not exist.")
                return []

            if e.status_code != 200:
                logger.error(
                    f"Error getting breeds by page {page}. Status code: {e.status_code}"
                )
                return []

        except RequestError as e:
            logger.error(f"Error getting breeds by page {page}. {e.message}")
            return []

        except HTTPError as e:
            if isinstance(e, TimeoutError):
                logger.error(
                    f"Timeout error getting breeds by page {page}. {e.message}"
                )

            if isinstance(e, NetworkError):
                logger.error(
                    f"Network error getting breeds by page {page}. {e.message}"
                )

            else:
                tb_str = f"Error getting breeds by page {page} " + "".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )
                logger.error(tb_str)

            return []

        try:
            data: dict | list = response.json()

        except Exception as e:
            logger.error(
                f"Error getting breeds by page {page}. {''.join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )}"
            )
            return []

        dto_response: DogBreedResponse = SerializerDTO(DogBreedResponse).serialize(data)

        self._records_count = dto_response.meta.pagination.records
        if self.records_page_count < page:
            logger.warning(
                f"The maximum number of breed pages has been exceeded. Max: {self.records_page_count}"
            )
            return []

        return dto_response.data

    def get_current_breed(self, id: str) -> BreedDataItem | None:
        try:
            response: ResponseLike = self._http_client.get(f"breeds/{id}")

        except HttpStatusError as e:
            if e.status_code != 200:
                logger.error(
                    f"Error getting breed with id {id}. Status code: {e.status_code}"
                )
                return None

        except RequestError as e:
            logger.error(f"Error getting breed with id {id}. {e.message}")
            return None

        except HTTPError as e:
            if isinstance(e, TimeoutError):
                logger.error(f"Timeout error getting breed with id {id}. {e.message}")

            if isinstance(e, NetworkError):
                logger.error(f"Network error getting breed with id {id}. {e.message}")

            else:
                tb_str = "".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )
                logger.error(tb_str)

            return None

        try:
            data: dict | list = response.json()

        except Exception as e:
            logger.error(
                f"Error getting breed with id {id}. {''.join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )}"
            )
            return None

        dto_response: DogCurrentBreedResponse = SerializerDTO(
            DogCurrentBreedResponse
        ).serialize(data)

        return dto_response
