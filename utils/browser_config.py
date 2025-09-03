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
        platform = os.getenv("platform", "desktop")  # Platform: desktop, mobile
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
                logging.info(f"Using device configuration for: {device_name}")
            else:
                logging.warning(
                    f"Device '{device_name}' not found, using default settings"
                )
        elif platform == "mobile":
            # Use mobile viewport when platform is mobile but no specific device
            context_options.update({
                "viewport": {"width": 375, "height": 812},
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
            })
            logging.info("Using mobile viewport configuration")
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

        return await self.browser.new_context(**context_options)

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


# Configure logging
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.CRITICAL)
