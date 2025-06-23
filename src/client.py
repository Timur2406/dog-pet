from .adapter.dogapi_httpx_client import DogAPIHTTPXClient
from .service import BreedService, FactService, GroupService
from httpx import Client


class DogAPIClient:
    def __init__(
        self,
        client: Client | None = None,
    ):
        self.http_client = DogAPIHTTPXClient(client=client)
        self.breeds = BreedService(self.http_client)
        self.facts = FactService(self.http_client)
        self.groups = GroupService(self.http_client)
