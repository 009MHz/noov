import os
import logging
import asyncio
from typing import Optional, Dict, Any, Union

import pytest
from utils.sess_handler import SessionHandler


# Type aliases for better readability
Playwright = Any
Browser = Any
BrowserContext = Any
Page = Any

# Configuration constants
DEFAULT_BROWSER = "chromium"

# Retry configuration
RETRY_ATTEMPTS = 3
RETRY_BASE_DELAY = 0.1
CONTEXT_RETRY_DELAY = 0.05

# Supported execution modes
SUPPORTED_MODES = ("pipeline", "local")


class Config:
    def __init__(self):
        """Initialize the browser configuration."""
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.session_handler: Optional[SessionHandler] = None
        self._playwright: Optional[Playwright] = None

    def is_headless(self) -> bool:
        return os.getenv("headless", "False").lower() == "true"

    def _get_browser_launch_args(self) -> Dict[str, Any]:
        args = []
        if not self.is_headless():
            args.extend([
                "--start-maximized",
                "--window-size=1920,1080",
                "--window-position=0,0"
            ])
        
        return {
            "headless": self.is_headless(),
            "args": args,
        }

    async def _launch_browser_with_retry(
        self, browser_type: str, launch_args: Dict[str, Any]
    ) -> None:
        """Launch browser with retry mechanism for race condition protection."""
        if not self._playwright:
            raise RuntimeError("Playwright instance not available")

        for attempt in range(RETRY_ATTEMPTS):
            try:
                self.browser = await self._playwright[browser_type].launch(**launch_args)
                return
            except Exception as e:
                if attempt == RETRY_ATTEMPTS - 1:
                    raise e
                await asyncio.sleep(RETRY_BASE_DELAY * (attempt + 1))

    async def setup_browser(self, playwright: Playwright) -> None:
        self._playwright = playwright
        browser_type = os.getenv("BROWSER", DEFAULT_BROWSER)
        mode = os.getenv("mode", "local")

        if mode not in SUPPORTED_MODES:
            raise ValueError(
                f"Unsupported execution mode: {mode}. Supported modes: {SUPPORTED_MODES}"
            )

        launch_args = self._get_browser_launch_args()
        await self._launch_browser_with_retry(browser_type, launch_args)

        # Initialize session handler
        self.session_handler = SessionHandler(self.browser, self.is_headless())
        logging.info("Browser setup completed successfully")

    def _get_device_config(self, platform: str, device_name: Optional[str] = None) -> Dict[str, Any]:
        """Get device configuration for the specified platform or device."""
        # If specific device requested, try to get it
        if device_name and self._playwright:
            device_config = self._playwright.devices.get(device_name)
            if device_config:
                return device_config

        # Get platform-specific configuration
        if platform == "mobile":
            return self._get_mobile_config()
        else:
            return self._get_desktop_config()

    def _get_mobile_config(self) -> Dict[str, Any]:
        """Get mobile configuration using native Playwright device or fallback."""
        if self._playwright:
            # Find any mobile device from Playwright's native devices
            for device_name, device_config in self._playwright.devices.items():
                if device_config.get("is_mobile", False):
                    return device_config
        
        # Fallback mobile config
        return {
            # "viewport": {"width": 375, "height": 667},
            # "screen": {"width": 375, "height": 667},
            "is_mobile": True, 
            "has_touch": True,
            "device_scale_factor": 1
        }

    def _get_desktop_config(self) -> Dict[str, Any]:
        """Get desktop configuration with 1920x1080 resolution."""
        return {
            "viewport": {"width": 1920, "height": 1080},
            "screen": {"width": 1920, "height": 1080},
            "is_mobile": False,
            "has_touch": False,
            "device_scale_factor": 1,
        }

    async def _create_context_with_retry(
        self, context_options: Dict[str, Any]
    ) -> BrowserContext:
        """Create browser context with retry mechanism for race condition protection."""
        if not self.browser:
            raise RuntimeError("Browser not initialized. Call setup_browser first.")

        for attempt in range(RETRY_ATTEMPTS):
            try:
                return await self.browser.new_context(**context_options)
            except Exception as e:
                if attempt == RETRY_ATTEMPTS - 1:
                    raise e
                await asyncio.sleep(CONTEXT_RETRY_DELAY * (attempt + 1))

    async def context_init(
        self,
        storage_state: Optional[str] = None,
        user_type: str = "user",
        device_name: Optional[str] = None,
    ) -> BrowserContext:

        if not self.browser or not self._playwright:
            raise RuntimeError("Browser not initialized. Call setup_browser first.")

        platform = os.getenv("platform", "desktop")
        context_options: Dict[str, Any] = {}

        # Get device configuration using simplified method
        context_options.update(self._get_device_config(platform, device_name))

        # Add session state if provided
        if storage_state and self.session_handler:
            session_state = await self.session_handler.create_session(user_type)
            if session_state:
                context_options["storage_state"] = session_state

        # Create context with retry mechanism
        return await self._create_context_with_retry(context_options)

    async def setup_page(self, device_name: Optional[str] = None) -> Page:
        context = await self.context_init(device_name=device_name)
        self.page = await context.new_page()
        return self.page

    async def setup_auth_page(
        self, auth_mode: str, device_name: Optional[str] = None
    ) -> Page:
        """
        Set up a new authenticated page with optional device emulation.

        Args:
            auth_mode: Authentication mode for session creation
            device_name: Optional device name for emulation

        Returns:
            Configured authenticated page instance

        Raises:
            RuntimeError: If session handler is not initialized
        """
        if not self.session_handler:
            raise RuntimeError(
                "Session handler not initialized. Call setup_browser first."
            )

        session_state = await self.session_handler.create_session(auth_mode)
        context = await self.context_init(
            storage_state=session_state, user_type=auth_mode, device_name=device_name
        )
        self.page = await context.new_page()
        return self.page

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
        # Try to get platform from parametrization
        platform = (getattr(request, "param", None) if hasattr(request, "param") else None)

        if not platform:
            try:
                platform = request.getfixturevalue("platform")
            except pytest.FixtureLookupError:
                platform = "desktop"  # safe default

        return platform

    async def create_context(self, request) -> tuple[BrowserContext, str]:
        platform = self._extract_platform_from_request(request)   # Extract platform from request

        os.environ["platform"] = platform

        # Create context - let the Config class handle device selection based on platform
        context = await self.runner.context_init()

        return context, platform

    async def create_page(self, context: BrowserContext) -> Page:
        page = await context.new_page()
        return page

    async def cleanup_page(self, page: Page) -> None:
        try:
            await self.runner.capture_handler()  # Capture screenshot if configured
            await page.close()
        except Exception as e:
            logging.warning(f"Error during page cleanup: {e}")

    async def cleanup_context(self, context: BrowserContext) -> None:
        try:
            await context.close()
        except Exception as e:
            logging.warning(f"Error during context cleanup: {e}")


def configure_logging() -> None:
    """Configure logging levels for browser automation components."""
    # Reduce noise from asyncio and filelock
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("filelock").setLevel(logging.CRITICAL)

    # Set appropriate level for browser config
    logging.getLogger(__name__).setLevel(logging.INFO)


configure_logging()
