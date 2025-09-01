import os, sys, json, shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
import pytest
from dotenv import load_dotenv

ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

load_dotenv(ROOT / ".env", override=False)

# ----------------- CLI options -----------------
def pytest_addoption(parser: pytest.Parser) -> None:
    g = parser.getgroup("ui")
    g.addoption("--base-url", action="store", default=os.getenv("BASE_URL", "https://noovoleum.com"))
    g.addoption("--video", action="store", default="retain-on-failure",
                choices=["off", "on", "retain-on-failure"])
    g.addoption("--screenshot", action="store", default="only-on-failure",
                choices=["off", "on", "only-on-failure"])
    g.addoption("--full-page-screenshot", action="store_true")
    g.addoption("--mock-map", action="store_true", help="Mock /open_api/boxes during UI tests")

# ----------------- Common session fixtures -----------------
@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    return str(pytestconfig.getoption("--base-url"))

@pytest.fixture(scope="session")
def artifacts_dir() -> Path:
    p = ROOT / "reports"
    p.mkdir(exist_ok=True)
    return p

@pytest.fixture(scope="session")
def video_mode(pytestconfig) -> str:
    return str(pytestconfig.getoption("--video"))

@pytest.fixture(scope="session")
def screenshot_mode(pytestconfig) -> str:
    return str(pytestconfig.getoption("--screenshot"))

@pytest.fixture(scope="session")
def full_page_screenshot(pytestconfig) -> bool:
    return bool(pytestconfig.getoption("--full-page-screenshot"))

@pytest.fixture(scope="session")
def env_name() -> str:
    return os.getenv("ENV", "prod").lower()

# ----------------- Allure environment file -----------------
@pytest.fixture(scope="session", autouse=True)
def write_allure_env():
    d = ROOT / "allure-results"
    d.mkdir(exist_ok=True)
    (d / "environment.properties").write_text(
        f"ENV={os.getenv('ENV','')}\n"
        f"BASE_URL={os.getenv('BASE_URL','')}\n"
        f"API_BASE={os.getenv('API_BASE','')}\n"
    )

# ----------------- Playwright API fixtures -----------------
@pytest.fixture(scope="session")
def api_base() -> str:
    return os.getenv("API_BASE", "https://api.noovoleum.com")

@pytest.fixture(scope="session")
def api_headers() -> dict:
    token = os.getenv("API_TOKEN", "").strip()
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

@pytest.fixture(scope="session")
def api_context(playwright, api_base: str, api_headers: dict):
    ctx = playwright.request.new_context(
        base_url=api_base,
        extra_http_headers=api_headers,
        timeout=float(os.getenv("REQUEST_TIMEOUT", "30")) * 1000,  # ms
    )
    yield ctx
    ctx.dispose()

# ----------------- UI fixtures -----------------
from playwright.sync_api import BrowserContext, Page

@pytest.fixture()
def context(browser, artifacts_dir: Path, video_mode: str) -> BrowserContext:
    video_dir: Optional[str] = None
    if video_mode in {"on", "retain-on-failure"}:
        vd = artifacts_dir / "videos"
        vd.mkdir(parents=True, exist_ok=True)
        video_dir = str(vd)
    ctx = browser.new_context(
        record_video_dir=video_dir if video_dir else None,
        viewport={"width": 1366, "height": 900},
        ignore_https_errors=True,
    )
    yield ctx
    ctx.close()

@pytest.fixture()
def page(context: BrowserContext,
         request: pytest.FixtureRequest,
         artifacts_dir: Path,
         video_mode: str,
         screenshot_mode: str,
         full_page_screenshot: bool,
         base_url: str) -> Page:
    p = context.new_page()
    p.set_default_timeout(10_000)
    setattr(p, "base_url", base_url)
    yield p

    # Determine outcome for artifact policy
    failed = any(getattr(request.node, a).failed
                 for a in ("rep_setup", "rep_call", "rep_teardown")
                 if hasattr(request.node, a))

    # Screenshots
    if screenshot_mode == "on" or (screenshot_mode == "only-on-failure" and failed):
        shots = artifacts_dir / "screenshots"
        shots.mkdir(parents=True, exist_ok=True)
        name = request.node.name.replace("/", "_")
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        p.screenshot(path=str(shots / f"{name}-{ts}.png"), full_page=full_page_screenshot)

    # Videos
    if video_mode in {"on", "retain-on-failure"}:
        try:
            vpath = p.video.path() if p.video else None
        except Exception:
            vpath = None
        if vpath:
            vd = artifacts_dir / "videos"
            vd.mkdir(parents=True, exist_ok=True)
            name = request.node.name.replace("/", "_")
            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
            dest = vd / f"{name}-{ts}.webm"
            shutil.move(vpath, dest)
            if video_mode == "retain-on-failure" and not failed and dest.exists():
                dest.unlink(missing_ok=True)

# Hook to access outcome inside fixtures
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
