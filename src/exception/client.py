from typing import Any


class HTTPError(Exception):
    """
    Base class for all HTTP exceptions
    """

    pass


class RequestError(HTTPError):
    """
    Base class for HTTP all request exceptions
    """

    def __init__(
        self, message: str, request_url: str, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(message, request_url)
        self.request_url = request_url
        self.message = message


class HttpStatusError(RequestError):
    """Class for exceptions with bad status code"""

    def __init__(self, message: str, status_code: int, request_url: str) -> None:
        super().__init__(message, request_url)
        self.status_code = status_code


class TimeoutError(RequestError):
    """Class for exceptions with timeout"""

    pass


class NetworkError(RequestError):
    """Class for exceptions with network error"""

    pass
