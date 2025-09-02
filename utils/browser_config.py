import os
import logging
from utils.sess_handler import SessionHandler


class Config:
    def __init__(self):
        self.browser = None
        self.page = None
        self.session_handler = None

    def is_headless(self):
        return os.getenv("headless") == "True"

    async def setup_browser(self, playwright):
        browser_type = os.getenv("BROWSER", "chromium")
        mode = os.getenv("mode")
        headless = self.is_headless()
        launch_args = {
            "headless": headless,
            "args": ["--start-maximized"]}

        if mode in ('pipeline', 'local'):
            self.browser = await playwright[browser_type].launch(**launch_args)
        elif mode == 'grid':
            server_url = "http://remote-playwright-server:4444"
            self.browser = await playwright[browser_type].connect(server_url)
        else:
            raise ValueError(f"Unsupported execution type: {mode}")

        self.session_handler = SessionHandler(self.browser, headless)

    async def context_init(self, storage_state=None, user_type="user"):
        context_options = {
            "viewport": {"width": 1920, "height": 1080} if self.is_headless() else None,
            "no_viewport": not self.is_headless()}

        if storage_state:
            context_options["storage_state"] = await self.session_handler.create_session(user_type)

        return await self.browser.new_context(**context_options)

    async def setup_page(self):
        context = await self.context_init()
        self.page = await context.new_page()
        return self.page

    async def setup_auth_page(self, auth_mode: str):
        context = await self.context_init(storage_state=True, user_type=auth_mode)
        self.page = await context.new_page()
        return self.page

    async def capture_handler(self):
        screenshot_option = os.getenv("screenshot", "off")
        if screenshot_option != "off" and self.page:
            screenshot_path = f"reports/screenshots/{await self.page.title()}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await self.page.screenshot(path=screenshot_path, full_page=True)


logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('filelock').setLevel(logging.CRITICAL)
