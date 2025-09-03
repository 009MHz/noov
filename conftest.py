import pytest
import os
import asyncio
import allure
from playwright.async_api import async_playwright
from utils.browser_config import Config, ContextManager
from utils.pytest_config import (
    pytest_generate_tests_handler as generate_tests_handler,
    configure_environment,
    add_pytest_options
)


def pytest_addoption(parser):
    """Add custom pytest command line options."""
    add_pytest_options(parser)


def pytest_configure(config):
    """Configure environment from CLI options."""
    configure_environment(config)


def pytest_generate_tests(metafunc):
    """Generate tests with platform parameters based on CLI options."""
    generate_tests_handler(metafunc)


@pytest.fixture(scope="function")
async def playwright():
    """Function-scoped playwright instance for worker safety."""
    async with async_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="function")
async def runner(playwright):
    """Function-scoped runner instance for parallel execution safety."""
    runner_instance = Config()
    await runner_instance.setup_browser(playwright)
    yield runner_instance
    if runner_instance.browser:
        await runner_instance.browser.close()


@pytest.fixture(scope="function")
async def browser(runner):
    """Function-scoped browser for parallel execution safety."""
    yield runner.browser


@pytest.fixture()
async def context(runner, request):
    """Create browser context with optional device emulation."""
    context_manager = ContextManager(runner)
    
    context, _ = await context_manager.create_context(request)
    yield context
    await context_manager.cleanup_context(context)


@pytest.fixture()
async def page(context, runner):
    """Create new page in the current context."""
    context_manager = ContextManager(runner)
    page = await context_manager.create_page(context)
    yield page
    await context_manager.cleanup_page(page)


@pytest.fixture()
async def user_auth(runner):
    page_instance = await runner.setup_auth_page("user")
    yield page_instance
    await runner.capture_handler()
    await page_instance.close()


@pytest.fixture()
async def admin_auth(runner):
    page_instance = await runner.setup_auth_page("admin")
    yield page_instance
    await runner.capture_handler()
    await page_instance.close()


@pytest.fixture()
async def super_auth(runner):
    page_instance = await runner.setup_auth_page("super_admin")
    yield page_instance
    await runner.capture_handler()
    await page_instance.close()


@pytest.fixture(scope="function")
async def api_request(playwright):
    """Create a basic APIRequestContext for testing.
    The actual URL and headers should be configured in the test files."""
    context = None
    try:
        context = await playwright.request.new_context(
            ignore_https_errors=True  # Useful for testing environments
        )
        yield context
    finally:
        if context:
            await context.dispose()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":  # if rep.when == "call" and rep.failed: # config on fail only
        screenshot_path = os.path.join("reports/screenshots", f"{item.name}.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

        try:
            page = item.funcargs.get('page') or item.funcargs.get('auth_page')
            if page:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(page.screenshot(path=screenshot_path, full_page=True))
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name="screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
