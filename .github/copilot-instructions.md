# Copilot Instructions for Test Automation Framework

## Goals (Scope & Priorities)

* Unified, **async-first** automation across **Web (Playwright)**, **API (Playwright request)**, and **Mobile (Appium)**.
* **POM** everywhere: intent-level methods in page/screens; assertions live in tests.
* **Deterministic** runs (no arbitrary sleeps). Prefer explicit waits/expectations.
* **Reportability** (Allure) and **repeatability** (CI matrix) as first-class.

## Framework Stack

* **Language**: Python **3.10+** with `async/await`
* **Web/UI**: Playwright (async), pytest
* **API**: Playwright request context (async)
* **Mobile**: Appium (Python client) via **async bridge** (see below)
* **Performance**: Locust (optional)
* **Pattern**: Page Object Model (POM) for web & mobile
* **Reporting**: Allure (local + GitHub Pages)
* **CI/CD**: GitHub Actions with browser/device matrix & artifacts

## Core Principles

1. **Scalability**: Multi-platform (web, api, mobile) with consistent conventions.
2. **Modularity**: POM + fixtures + utilities—clean separation of concerns.
3. **Maintainability**: Modern locators, minimal coupling, typed helpers.
4. **Quality**: Type hints, meaningful errors/logging, parallel by default.
5. **Continuous Validity**: On every change, tests run in local first; block merges on red.

## Project Structure (authoritative)

```
### Project Structure
```
noovoleum/
├── .auth/                          # Authentication configurations
├── .github/                        # GitHub configurations
│   ├── workflows/                  # GitHub Actions workflows
│   └── copilot-instructions.md     # GitHub Copilot instructions
├── .venv/                          # Python virtual environment
├── reports/                        # Test execution reports
├── tests/                          # Test suites
│   ├── api/                        # API tests
│   ├── web/                        # Web UI tests
│   │   ├── admin/                  # Admin portal tests
│   │   │   ├── dashboard/          # Dashboard tests (empty)
│   │   │   └── login_portal/       # Login portal tests
│   │   └── client/                 # Client-facing tests
│   ├── mobile/                     # Mobile app tests
│   │   ├── android/                # Android-specific tests
│   │   └── ios/                    # iOS-specific tests
│   ├── performance/                # Performance tests
│   │   └── locustfile.py           # Locust performance test file
│   └── fixtures/                   # Test fixtures
│       └── login_fixtures.py       # Login-related fixtures
├── sources/                        # Page objects and clients
│   ├── web/                        # Web page objects
│   │   ├── admin/                  # Admin portal page objects
│   │   └── client/                 # Client-facing page objects
│   ├── mobile/                     # Mobile app page objects
│   │   ├── android/                # Android page objects
│   │   └── ios/                    # iOS page objects
│   └── api/                        # API clients
│       ├── __base.py               # Base API client
│       └── clients/                # API client implementations
├── utils/                          # Shared utilities            
├── .env                            # Environment variables
├── .gitignore                      # Git ignore rules
├── conftest.py                     # pytest configuration
├── pytest.ini                     # pytest settings
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies
```

## Development Standards

### Async Everywhere (with Mobile Bridge)

* **Web/API**: native async (Playwright).
* **Mobile (Appium)**: Appium’s Python client is sync. Wrap calls in an **async bridge** (`asyncio.to_thread` or `anyio.to_thread.run_sync`) so tests & fixtures **remain async**.

**Pattern (async bridge helper):**

```python
# utils/async_bridge.py
from asyncio import to_thread
def aify(fn):
    async def _inner(*args, **kwargs):
        return await to_thread(fn, *args, **kwargs)
    return _inner
```

**Use in a screen object:**

```python
# sources/mobile/android/login_screen.py
from utils.async_bridge import aify

class AndroidLoginScreen:
    def __init__(self, driver):  # driver: appium.webdriver.Remote
        self.driver = driver

    @property
    def email(self):
        return self.driver.find_element("accessibility id", "emailInput")

    @property
    def password(self):
        return self.driver.find_element("accessibility id", "passwordInput")

    @aify
    def _type_email(self, value: str):
        self.email.clear(); self.email.send_keys(value)

    @aify
    def _type_password(self, value: str):
        self.password.clear(); self.password.send_keys(value)

    @aify
    def _tap_login(self):
        self.driver.find_element("accessibility id", "loginButton").click()

    async def login_as(self, email: str, password: str):
        await self._type_email(email)
        await self._type_password(password)
        await self._tap_login()
```

> Copilot: when generating **mobile** code, always keep **tests async** and **wrap driver calls** with the bridge. Never block the event loop with raw sleeps.

### POM Rules (Web & Mobile)

* Expose **intent methods** (e.g., `login_as`, `filter_by_status`, `open_drawer`).
* Keep **assertions in tests**, not in page/screen classes.
* Return **data/locators/states** from POM for the test to assert.
* Prefer **composition** over inheritance. Create small, well-named helpers.

### Locators & Interactions (Web)

Order of preference:

1. `get_by_role(name=...)`
2. `get_by_label(...)`, `get_by_placeholder(...)`
3. `get_by_test_id(...)`
4. `get_by_text(...)` (scoped to a container)
5. Minimal CSS fallback (avoid brittle selectors; avoid XPath unless necessary)

**Expectations**:

* Use `expect(...)` for stability (visibility, URL, text, attributes).
* No `time.sleep`. If needed, do targeted waits (e.g., `expect(locator).to_be_visible()` when visibility is the behavior under test).

### API Testing

* Use Playwright’s `request.new_context()` fixture.
* Centralize base URL/headers and token/session handling.
* Validate status, structure, and critical fields (schema helpers optional).

### Test Structure & Naming

* Files: `tests/<platform>/<area>/test_<feature>.py`
* Inside tests: **AAA** (Arrange–Act–Assert) with blank lines separating sections.
* Keep tests ≤ 60 LOC when possible; split flows rather than build “mega-tests.”

### Type Hints & Docs

* Type annotate POM interfaces and fixtures.
* Docstring complex flows; skip obvious one-liners.

### Error Handling & Logging

* Raise meaningful exceptions in helpers (e.g., domain errors).
* Capture artifacts on failure: screenshot, console, trace (web); driver logs/screenshots (mobile).

## Fixtures & Environment

### Web & API (async)

* `page` fixture (headless controlled by env; default headless in CI).
* `auth_context` or storage state fixture for explicit session reuse.
* `request_context` fixture for API with base URL & headers.

### Mobile (Appium) – async wrapper fixture

```python
# tests/fixtures/appium_fixtures.py
import os, asyncio
import pytest
from appium import webdriver
from utils.async_bridge import aify

@pytest.fixture
async def android_driver():
    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": os.getenv("ANDROID_DEVICE", "emulator-5554"),
        "app": os.getenv("ANDROID_APP_APK"),  # path or app package/activity if preinstalled
        "newCommandTimeout": 120
    }
    def _create():
        return webdriver.Remote(os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723/wd/hub"), caps)
    driver = await asyncio.to_thread(_create)
    yield driver
    await asyncio.to_thread(driver.quit)
```

> Copilot: When generating mobile tests, inject `android_driver`/`ios_driver`, build POM screens, call intent methods with `await` (they’re async thanks to the bridge).

## Assertions (Canonical)

* **Keep all assertions in tests.**
* Prefer `expect` (web) and deterministic state checks (mobile API responses, UI states).
* URL checks: `expect(page).to_have_url(...)`.
* Counts: `expect(locator).to_have_count(n)`.
* Text: `to_have_text` (exact) vs `to_contain_text` (partial).

## Execution & CI/CD

### Local Commands (suggest defaults)

```bash
# Install
pip install -r requirements.txt
playwright install

# Web UI
pytest tests/web -m ui --alluredir=./reports/allure-results

# API
pytest tests/api -m api --alluredir=./reports/allure-results

# Mobile (Appium server must be running; ANDROID_* env prepared)
pytest tests/mobile -m mobile --alluredir=./reports/allure-results

# Allure
allure generate ./reports/allure-results -o ./reports/allure-report --clean
```

### GitHub Actions (expectations)

* Matrix: `{ browser: [chromium, firefox, webkit] }` for web; optional `{ mobile: [android, ios] }` job(s) gated behind labels or separate workflow.
* Install: `playwright install --with-deps`
* Cache: pip & browsers
* Artifacts: `allure-results`, screenshots, videos, Playwright trace
* Deploy Allure to GH Pages on `main`

## Pull Request Checklist (Copilot must enforce)

* Tests added/updated; fast & deterministic
* POM methods expose **intent**; no assertions inside POM
* Async-safe: no blocking sleeps; mobile wrapped with async bridge
* Env-aware; secrets not committed
* Lint/type checks pass (ruff/flake8/mypy if present)
* CI green; artifacts uploaded; docs/README updated if needed

## Copilot Prompt Patterns (use verbatim as templates)

**Add a Web Page Object**

> Create `sources/web/admin/login_page.py` with intent methods: `open()`, `login_as(email, password)`. Prefer `get_by_role`, then `get_by_label`. Return essential locators/data but no assertions. Add docstrings and type hints.

**Create a Web Test**

> Create `tests/web/admin/login_portal/test_login_success.py`. Use async Playwright fixtures, AAA, and `expect(page).to_have_url("/dashboard")` after `LoginPage.login_as(...)`. Keep ≤60 LOC.

**Add an API Test**

> Create `tests/api/test_admin_login.py` using `request_context` fixture. POST `/admin/login`, assert 200 and presence of `token`. No sleeps; add minimal schema check helper if available.

**Add an Android Screen + Test**

> Create `sources/mobile/android/login_screen.py` using the async bridge (`aify`) to wrap driver calls. Intent method: `login_as(email, password)`. Then create `tests/mobile/android/test_login_flow.py` using `android_driver` fixture and assert landing activity/text (assertions in test only).

## Non-Goals & Gotchas

* ❌ No arbitrary `time.sleep`—ever.
* ❌ Don’t couple selectors to visual libraries (e.g., raw MUI classnames).
* ❌ Don’t put assertions inside POM/screen classes.
* ⚠️ Appium remains sync under the hood—**always** go through the async bridge in async tests.
* ⚠️ For flakiness: prefer role/label/testid; add explicit waits only when behavior demands it.

---

## Minimal Examples (for Copilot grounding)

**Web POM snippet (async):**

```python
# sources/web/admin/login_page.py
from playwright.async_api import Page, Locator

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email:  Locator = page.get_by_label("Email")
        self.password: Locator = page.get_by_label("Password")
        self.login_btn: Locator = page.get_by_role("button", name="Login")

    async def open(self) -> None:
        await self.page.goto("/login")

    async def login_as(self, email: str, password: str) -> None:
        await self.email.fill(email)
        await self.password.fill(password)
        await self.login_btn.click()
```

**Android test skeleton (async):**

```python
# tests/mobile/android/test_login_flow.py
import pytest
from sources.mobile.android.login_screen import AndroidLoginScreen

@pytest.mark.mobile
@pytest.mark.android
async def test_login_success(android_driver):
    screen = AndroidLoginScreen(android_driver)
    await screen.login_as("user@example.com", "secret")
    # Assertions: verify next screen state (fetch element text via async bridge if needed)
    # Example (wrapped in screen helper returning a string):
    # greeting = await screen.get_greeting_text()
    # assert "Welcome" in greeting
```
