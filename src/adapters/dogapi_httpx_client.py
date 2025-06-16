from typing import Any
from interfaces.http_client import HTTPClient
from httpx import Client, Response

from src.config import Settings


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
        params: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Default HTTPX GET method implementation
        """
        response: Response = self.client.get(url=endpoint, params=params, **kwargs)
        response.raise_for_status()
        return response

    def post(
        self,
        endpoint: str,
        params: dict | None = None,
        json: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Default HTTPX POST method implementation
        """
        response: Response = self.client.post(
            url=endpoint, params=params, json=json, **kwargs
        )
        response.raise_for_status()
        return response

    def put(
        self,
        endpoint: str,
        params: dict | None = None,
        json: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Default HTTPX PUT method implementation
        """
        response: Response = self.client.put(
            url=endpoint, params=params, json=json, **kwargs
        )
        response.raise_for_status()
        return response

    def delete(
        self,
        endpoint: str,
        params: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Default HTTPX DELETE method implementation
        """
        response: Response = self.client.delete(url=endpoint, params=params, **kwargs)
        response.raise_for_status()
        return response

    def _close(self) -> None:
        if self._client is not None:
            self._client.close()

    def __del__(self) -> None:
        self._close()
