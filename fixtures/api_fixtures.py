import pytest
from playwright.async_api import async_playwright

# If you already have a config loader, import and use it; hardcode for brevity:
API_BASE = "https://api.noovoleum.com"

@pytest.fixture(scope="session")
async def pw():
    async with async_playwright() as p:
        yield p

@pytest.fixture(scope="session")
async def api_context(pw):
    ctx = await pw.request.new_context(
        base_url=API_BASE,
        extra_http_headers={
            "Accept": "application/json",
            # "Authorization": f"Bearer {os.getenv('API_TOKEN')}"  # if needed later
        },
        timeout=30_000,  # 30s default timeout
    )
    yield ctx
    await ctx.dispose()
