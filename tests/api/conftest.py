import pytest
from playwright.sync_api import Playwright, APIRequestContext

BASE_API = "https://api.noovoleum.com"

@pytest.fixture(scope="session")
def api_request(playwright: Playwright) -> APIRequestContext:
    ctx = playwright.request.new_context(
        base_url=BASE_API,
        extra_http_headers={"Accept": "application/json"},
        timeout=30_000,  # 30s
    )
    yield ctx
    ctx.dispose()
