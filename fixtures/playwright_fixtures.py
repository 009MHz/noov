import pytest
from playwright.async_api import async_playwright
from libs.config_loader import load_settings

@pytest.fixture(scope="session")
async def pw():
    async with async_playwright() as p:
        yield p

@pytest.fixture(scope="session")
async def browser(pw, request):
    s = load_settings(env=request.config.getoption("--env"))
    browser = await pw.chromium.launch(headless=s.headless)
    yield browser
    await browser.close()

@pytest.fixture(scope="function")
async def context(browser):
    ctx = await browser.new_context()
    yield ctx
    await ctx.close()

@pytest.fixture(scope="function")
async def page(context):
    page = await context.new_page()
    yield page