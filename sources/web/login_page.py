from playwright.async_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    async def open(self, base_url: str):
        await self.page.goto(f"{base_url}/login")

    async def login(self, email: str, password: str):
        await self.page.get_by_label("Email").fill(email)
        await self.page.get_by_label("Password").fill(password)
        await self.page.get_by_role("button", name="Sign in").click()