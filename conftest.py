import os
import pathlib
import contextlib
import pytest
import allure
from playwright.sync_api import sync_playwright

HEADLESS = False
VIEWPORT = {"width": 1920, "height": 1080}
REPORTS_DIR = pathlib.Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright, browser_name):  # browser_name comes from pytest-playwright
    launch_args = {}
    if browser_name == "chromium":
        launch_args["args"] = ["--start-maximized"]
    b = getattr(playwright, browser_name).launch(headless=HEADLESS, **launch_args)
    yield b
    b.close()

@pytest.fixture(scope="function")
def context(browser, browser_name, request, tmp_path_factory):
    ctx = browser.new_context(
        viewport=VIEWPORT,
        record_video_dir=None,
    )
    # trace on first retry
    execution_count = getattr(request.node, "execution_count", 1)
    if execution_count > 1:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=False)
    yield ctx
    with contextlib.suppress(Exception):
        if ctx.tracing.is_tracing():
            trace_path = tmp_path_factory.mktemp("traces") / f"{request.node.name}-{browser_name}.zip"
            ctx.tracing.stop(path=str(trace_path))
            if trace_path.exists():
                allure.attach.file(
                    str(trace_path),
                    name=f"trace-{request.node.name}-{browser_name}",
                    attachment_type=allure.attachment_type.ZIP,
                )
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    with contextlib.suppress(Exception):
        page.evaluate("() => window.moveTo(0,0); window.resizeTo(screen.width, screen.height);")
    yield page
    page.close()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield                          # let other hooks run
    rep = outcome.get_result()               # TestReport

    # Guard: only after the test body ("call") and only on failure
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        browser_name = item.funcargs.get("browser_name", "browser")
        if page:
            try:
                png_path = pathlib.Path("reports") / f"{item.name}-{browser_name}.png"
                page.screenshot(path=str(png_path), full_page=False)
                allure.attach.file(
                    str(png_path),
                    name=f"screenshot-{item.name}-{browser_name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
