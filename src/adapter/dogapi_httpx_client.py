from typing import Any
from src.interface.http_client import HTTPClient, ResponseLike
from httpx import (
    Client,
    Response,
    HTTPStatusError,
    TimeoutException,
    NetworkError,
    HTTPError,
    RequestError,
)

from src.config import Settings
from src.exception import (
    HttpStatusError as DogAPIHttpStatusError,
    TimeoutError as DogAPITimeoutError,
    NetworkError as DogAPINetworkError,
    HTTPError as DogAPIClientError,
    RequestError as DogAPIRequestError,
)


class DogAPIHTTPXClient(HTTPClient):
    """HTTPX Client implementation"""

    def __init__(self, client: Client | None = None):
        self.base_url = Settings.BASE_URL
        self._client: Client | None = client

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(
                base_url=self.base_url, headers={"accept": "application/json"}
            )
        return self._client

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        **kwargs: dict[str, Any],
    ) -> ResponseLike:
        """
        Default HTTPX GET method implementation
        """
        try:
            response: Response = self.client.get(
                url=endpoint,
                params=params,
            )
            response.raise_for_status()
            return response
        except HTTPStatusError as e:
            raise DogAPIHttpStatusError(
                message=str(e),
                status_code=e.response.status_code,
                request_url=str(e.request.url),
            ) from e
        except TimeoutException as e:
            raise DogAPITimeoutError(
                message=str(e), request_url=str(e.request.url)
            ) from e
        except NetworkError as e:
            raise DogAPINetworkError(
                message=str(e), request_url=str(e.request.url)
            ) from e
        except RequestError as e:
            raise DogAPIRequestError(
                message=str(e), request_url=str(e.request.url)
            ) from e
        except HTTPError as e:
            raise DogAPIClientError from e

    def _close(self) -> None:
        if self._client is not None:
            self._client.close()

    def __del__(self) -> None:
        self._close()
