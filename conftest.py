import os
import pathlib
import contextlib
from typing import Dict, Any

import pytest
import allure

# Directories
REPORTS_DIR = pathlib.Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Defaults
VIEWPORT = {"width": 1920, "height": 1080}

# ---------------- CLI option ----------------
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headless",
        action="store_true",
        help="Force headless mode (defaults to headless on CI anyway).",
    )

# ---------------- Session-level helpers ----------------
@pytest.fixture(scope="session")
def is_headless(pytestconfig) -> bool:
    """
    Headless resolution order:
    1) --headless flag
    2) CI=true environment => headless
    3) default: headed locally (False)
    """
    if pytestconfig.getoption("--headless"):
        return True
    if os.getenv("CI", "").lower() in ("1", "true", "yes"):
        return True
    return False

# ---------------- Browser / Context / Page ----------------
# Use pytest-playwright's built-in 'playwright' and 'browser_name' fixtures.
# We create our own browser based on headless + per-browser launch args.
@pytest.fixture(scope="session")
def browser(playwright, browser_name, is_headless):
    launch_args: Dict[str, Any] = {"headless": is_headless}
    if browser_name == "chromium":
        # Helpful flags for CI stability
        launch_args.setdefault("args", [])
        launch_args["args"].extend([
            "--start-maximized",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ])
    b = getattr(playwright, browser_name).launch(**launch_args)
    yield b
    b.close()

@pytest.fixture(scope="function")
def context(browser, request):
    ctx = browser.new_context(
        viewport=VIEWPORT,             # Keep a fixed viewport for consistency
        record_video_dir=None,         # Add a dir if you want videos
        ignore_https_errors=True,      # Toggle if your env needs it
    )

    # Start tracing only on retries (execution_count > 1 is set by rerun plugin)
    tracing_started = False
    execution_count = getattr(request.node, "execution_count", 1)
    if execution_count > 1:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=False)
        tracing_started = True

    yield ctx

    # Stop/attach tracing on teardown if started
    if tracing_started:
        trace_dir = pathlib.Path(".pytest-traces")
        trace_dir.mkdir(exist_ok=True, parents=True)
        trace_path = trace_dir / f"{request.node.name}-{browser.browser_type.name}.zip"
        with contextlib.suppress(Exception):
            ctx.tracing.stop(path=str(trace_path))
            if trace_path.exists():
                allure.attach.file(
                    str(trace_path),
                    name=f"trace-{request.node.name}-{browser.browser_type.name}",
                    attachment_type=allure.attachment_type.ZIP,
                )
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    p = context.new_page()
    # Best-effort maximize in headed; ignored in headless
    with contextlib.suppress(Exception):
        p.evaluate("() => { try { window.moveTo(0,0); window.resizeTo(screen.width, screen.height); } catch(e){} }")
    yield p
    p.close()

# ---------------- Failure screenshot hook ----------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Only after the test body and only on failure
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        browser_name = item.funcargs.get("browser_name", "browser")
        if page:
            png_path = REPORTS_DIR / f"{item.name}-{browser_name}.png"
            with contextlib.suppress(Exception):
                page.screenshot(path=str(png_path), full_page=False)
                allure.attach.file(
                    str(png_path),
                    name=f"screenshot-{item.name}-{browser_name}",
                    attachment_type=allure.attachment_type.PNG,
                )
