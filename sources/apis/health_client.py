from typing import Optional
import httpx


class HealthClient:
    def __init__(self, client: httpx.Client):
        self.client = client

    def health(self) -> httpx.Response:
        return self.client.get("/health")
