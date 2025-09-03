import os
import logging
import pytest
from typing import Optional, Dict, Any
from utils.sess_handler import SessionHandler
import asyncio


# Type hints from playwright are used through type annotations
Playwright = Any  # type: ignore
Browser = Any  # type: ignore
BrowserContext = Any  # type: ignore
Page = Any  # type: ignore


class Config:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.session_handler: Optional[SessionHandler] = None
        self._playwright: Optional[Playwright] = None

    def is_headless(self) -> bool:
        return os.getenv("headless") == "True"

    async def setup_browser(self, playwright: Playwright):
        """Initialize browser with playwright instance with retry for race conditions."""
        self._playwright = playwright
        browser_type = os.getenv("BROWSER", "chromium")
        mode = os.getenv("mode", "local")  # Execution mode: local, grid, pipeline
        headless = self.is_headless()
        launch_args = {"headless": headless, "args": ["--start-maximized"]}

        if mode in ("pipeline", "local"):
            # Add retry mechanism for race conditions in parallel execution
            for attempt in range(3):
                try:
                    self.browser = await playwright[browser_type].launch(**launch_args)
                    break
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        raise e
                    await asyncio.sleep(0.1 * (attempt + 1))  # Exponential backoff
        else:
            raise ValueError(f"Unsupported execution type: {mode}")

        self.session_handler = SessionHandler(self.browser, headless)

    async def context_init(
        self,
        storage_state: Optional[str] = None,
        user_type: str = "user",
        device_name: Optional[str] = None,
    ) -> BrowserContext:
        """Initialize browser context with optional device emulation."""
        if not self.browser or not self._playwright:
            raise RuntimeError("Browser not initialized. Call setup_browser first.")

        context_options: Dict[str, Any] = {}
        platform = os.getenv("platform", "desktop")

        if device_name:
            # Get device configuration from Playwright's predefined devices
            device = self._playwright.devices.get(device_name)
            if device:
                context_options.update(device)
            else:
                available_devices = list(self._playwright.devices.keys())
                mobile_devices = [
                    d
                    for d in available_devices
                    if "iPhone" in d or "Pixel" in d or "Galaxy" in d
                ][:5]
                logging.warning(
                    f"Device '{device_name}' not found. Available mobile devices: {mobile_devices}"
                )

                # Fallback to default mobile configuration
                context_options.update(
                    {
                        "viewport": {"width": 375, "height": 812},
                        "is_mobile": True,
                        "has_touch": True,
                    }
                )
        elif platform == "mobile":
            context_options.update(
                {
                    "is_mobile": True,
                    "has_touch": True,
                }
            )
        else:
            # Desktop defaults when platform is desktop
            context_options.update(
                {
                    "viewport": (
                        {"width": 1920, "height": 1080} if self.is_headless() else None
                    ),
                    "no_viewport": not self.is_headless(),
                }
            )

        if storage_state and self.session_handler:
            session_state = await self.session_handler.create_session(user_type)
            if session_state:
                context_options["storage_state"] = session_state

        for attempt in range(3):
            try:
                return await self.browser.new_context(**context_options)
            except Exception as e:
                if attempt == 2:  # Last attempt
                    raise e
                await asyncio.sleep(
                    0.05 * (attempt + 1)
                )  # Small delay for race conditions

    async def setup_page(self, device_name: Optional[str] = None) -> Page:
        """Set up a new page with optional device emulation."""
        context = await self.context_init(device_name=device_name)
        self.page = await context.new_page()
        return self.page

    async def setup_auth_page(
        self, auth_mode: str, device_name: Optional[str] = None
    ) -> Page:
        """Set up a new authenticated page with optional device emulation."""
        if not self.session_handler:
            raise RuntimeError("Session handler not initialized")

        session_state = await self.session_handler.create_session(auth_mode)
        context = await self.context_init(
            storage_state=session_state, user_type=auth_mode, device_name=device_name
        )
        self.page = await context.new_page()
        return self.page

    async def capture_handler(self):
        """Handle screenshot capture based on environment settings."""
        screenshot_option = os.getenv("screenshot", "off")
        if screenshot_option != "off" and self.page:
            screenshot_path = f"reports/screenshots/{await self.page.title()}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await self.page.screenshot(path=screenshot_path, full_page=True)


class ContextManager:
    """Handles browser context creation and management."""

    def __init__(self, runner: Config):
        self.runner = runner

    async def create_context(self, request):
        """Create browser context with optional device emulation."""
        device_name = None

        # Get platform from parametrize or environment
        platform = (
            getattr(request, "param", None) if hasattr(request, "param") else None
        )
        if not platform:
            try:
                platform = request.getfixturevalue("platform")
            except pytest.FixtureLookupError:
                platform = "desktop"  # default

        # Set platform in environment for browser config
        os.environ["platform"] = platform

        # Check for mobile marker and device parameter
        if request.node.get_closest_marker("mobile"):
            try:
                # Try to get device name from parametrize
                device_name = request.getfixturevalue("device_name")
            except pytest.FixtureLookupError:
                # Use modern default devices if not specified
                device_name = "Pixel 7"  # Modern Android device

            logging.info(f"Setting up mobile context with device: {device_name}")
        elif platform == "mobile":
            # Set default mobile device for mobile platform
            device_name = "iPhone XR"
            logging.info(
                f"Setting up mobile context with default device: {device_name}"
            )

        # Initialize context with device if specified
        context = await self.runner.context_init(device_name=device_name)
        return context, platform

    async def create_page(self, context):
        """Create new page in the current context."""
        page = await context.new_page()
        return page

    async def cleanup_page(self, page):
        """Clean up page resources."""
        await self.runner.capture_handler()  # Capture screenshot if configured
        await page.close()

    async def cleanup_context(self, context):
        """Clean up context resources."""
        await context.close()


# Configure logging
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.CRITICAL)
