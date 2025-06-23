from .adapter.dogapi_httpx_client import DogAPIHTTPXClient
from .service import BreedService, FactService, GroupService
from httpx import Client


class DogAPIClient:
    def __init__(
        self,
        client: Client | None = None,
    ) -> None:
        self.http_client: DogAPIHTTPXClient = DogAPIHTTPXClient(client=client)
        self.breeds: BreedService[DogAPIHTTPXClient] = BreedService(self.http_client)
        self.facts: FactService[DogAPIHTTPXClient] = FactService(self.http_client)
        self.groups: GroupService[DogAPIHTTPXClient] = GroupService(self.http_client)
