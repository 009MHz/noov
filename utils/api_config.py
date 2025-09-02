import os
from urllib.parse import urljoin

class APIConfig:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "https://api.noovoleum.com")

    def get_url(self, endpoint: str) -> str:
        """
        Construct a full URL from the base URL and endpoint.
        Ensures the URL is properly formatted regardless of slashes.
        """
        # Remove leading/trailing slashes from endpoint
        endpoint = endpoint.strip('/')
        # Ensure base_url ends with a slash
        base = self.base_url.rstrip('/') + '/'
        # Join the URLs properly
        return urljoin(base, endpoint)

# Create a singleton instance
api_config = APIConfig()
