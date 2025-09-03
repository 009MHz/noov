import os
import logging
import asyncio
from typing import Optional, Dict, Any

import pytest
from utils.sess_handler import SessionHandler

# Constants
DEFAULT_BROWSER = "chromium"
DEFAULT_DEVICES = "Pixel 9"
RETRY_ATTEMPTS = 3
RETRY_DELAY = 0.1
SUPPORTED_MODES = ("pipeline", "local")


class Config:   
    def __init__(self):
        """Initialize browser configuration."""
        self.browser = None
        self.page = None
        self.session_handler = None
        self._playwright = None

    def is_headless(self) -> bool:
        return os.getenv("headless", "False").lower() == "true"

    def _get_browser_launch_args(self) -> Dict[str, Any]:
        args = (
            ["--start-maximized", "--window-size=1920,1080"]
            if not self.is_headless()
            else []
        )
        return {"headless": self.is_headless(), "args": args}

    async def _retry_operation(self, operation, *args, **kwargs):
        """Generic retry wrapper for browser operations."""
        for attempt in range(RETRY_ATTEMPTS):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                if attempt == RETRY_ATTEMPTS - 1:
                    raise e
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))

    async def setup_browser(self, playwright) -> None:
        self._playwright = playwright
        browser_type = os.getenv("BROWSER", DEFAULT_BROWSER)
        mode = os.getenv("mode", "local")

        if mode not in SUPPORTED_MODES:
            raise ValueError(f"Unsupported mode: {mode}. Supported: {SUPPORTED_MODES}")

        launch_args = self._get_browser_launch_args()
        self.browser = await self._retry_operation(
            playwright[browser_type].launch, **launch_args
        )
        self.session_handler = SessionHandler(self.browser, self.is_headless())

    def _get_device_config(
        self, platform: str, device_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get device configuration for platform."""
        if device_name and self._playwright:
            config = self._playwright.devices.get(device_name)
            if config:
                return config

        if platform == "mobile":
            return self._get_mobile_config()
        return {
            "viewport": {"width": 1920, "height": 1080},
            "is_mobile": False,
            "has_touch": False,
        }

    def _get_mobile_config(self) -> Dict[str, Any]:
        if self._playwright:
            default_device = self._playwright.devices.get(DEFAULT_DEVICES)  # Param to receive selected device
            if default_device:
                return default_device

        # Fallback mobile config if Pixel 9 not available
        return {
            "viewport": {"width": 414, "height": 915},
            "screen": {"width": 414, "height": 915},
            "is_mobile": True, 
            "has_touch": True,
            "device_scale_factor": 2,
        }

    async def context_init(
        self,
        storage_state: Optional[str] = None,
        user_type: str = "user",
        device_name: Optional[str] = None,
    ):
        """Initialize browser context with device emulation."""
        if not self.browser:
            raise RuntimeError("Browser not initialized. Call setup_browser first.")

        platform = os.getenv("platform", "desktop")
        context_options = self._get_device_config(platform, device_name)

        if storage_state and self.session_handler:
            session_state = await self.session_handler.create_session(user_type)
            if session_state:
                context_options["storage_state"] = session_state

        context = await self._retry_operation(
            self.browser.new_context, **context_options
        )
        return context

    async def setup_page(self, device_name: Optional[str] = None):
        """Set up a new page with device emulation."""
        context = await self.context_init(device_name=device_name)
        if context:
            self.page = await context.new_page()
            return self.page
        raise RuntimeError("Failed to create context")

    async def setup_auth_page(self, auth_mode: str, device_name: Optional[str] = None):
        """Set up authenticated page with device emulation."""
        if not self.session_handler:
            raise RuntimeError("Session handler not initialized.")

        session_state = await self.session_handler.create_session(auth_mode)
        context = await self.context_init(session_state, auth_mode, device_name)
        if context:
            self.page = await context.new_page()
            return self.page
        raise RuntimeError("Failed to create authenticated context")

    async def capture_handler(self) -> None:
        """
        Handle screenshot capture based on environment settings.

        Creates screenshots in reports/screenshots/ directory if screenshot option is enabled.
        """
        screenshot_option = os.getenv("screenshot", "off").lower()

        if screenshot_option == "off" or not self.page:
            return

        try:
            page_title = await self.page.title()
            # Sanitize filename
            safe_title = "".join(
                c for c in page_title if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            screenshot_path = f"reports/screenshots/{safe_title or 'untitled'}.png"

            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await self.page.screenshot(path=screenshot_path, full_page=True)
        except Exception as e:
            logging.warning(f"Failed to capture screenshot: {e}")


class ContextManager:
    def __init__(self, runner: Config):
        self.runner = runner

    def _extract_platform_from_request(self, request) -> str:
        """Extract platform from pytest request."""
        platform = getattr(request, "param", None)
        if not platform:
            try:
                platform = request.getfixturevalue("platform")
            except pytest.FixtureLookupError:
                platform = "desktop"
        return platform

    async def create_context(self, request):
        """Create context with platform detection."""
        platform = self._extract_platform_from_request(request)
        os.environ["platform"] = platform
        context = await self.runner.context_init()
        return context, platform

    async def create_page(self, context):
        return await context.new_page()

    async def cleanup_page(self, page) -> None:
        try:
            await self.runner.capture_handler()
            await page.close()
        except Exception as e:
            logging.warning(f"Page cleanup error: {e}")

    async def cleanup_context(self, context) -> None:
        try:
            await context.close()
        except Exception as e:
            logging.warning(f"Context cleanup error: {e}")


def configure_logging() -> None:
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("filelock").setLevel(logging.CRITICAL)
    logging.getLogger(__name__).setLevel(logging.INFO)


configure_logging()
