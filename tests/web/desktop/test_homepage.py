import pytest
import allure
from playwright.async_api import expect
from sources.web.home_page import HomePage

@allure.epic("Marketing Site")
@allure.feature("Homepage")
@pytest.mark.asyncio
@pytest.mark.smoke
async def test_homepage_logo_and_heading(page):
    home = HomePage(page)

    with allure.step("Open homepage and verify key UI is visible"):
        await home.open("https://noovoleum.com")
        await expect(home.logo).to_be_visible()
        await expect(home.hero_text).to_be_visible()

    with allure.step("Basic sanity: page title present"):
        # this is optional—adjust to your real title if you want strict match
        title = await page.title()
        assert isinstance(title, str) and len(title) > 0
