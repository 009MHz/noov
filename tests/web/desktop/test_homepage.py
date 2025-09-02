import pytest
import allure
from playwright.async_api import expect
from sources.web.home_page import HomePage
from allure import severity_level as severity


@pytest.fixture(scope='function')
async def home(page):
    home = HomePage(page)
    await home.open("https://noovoleum.com")
    return home


@allure.epic("Marketing Site")
@allure.feature("Homepage")
@pytest.mark.ui
@pytest.mark.asyncio
@pytest.mark.smoke
class TestHomepage:
    @pytest.mark.smoke
    @allure.title("First State Login Page Validation")
    @allure.feature("Login/ Email", "Login/ Google")
    @allure.severity(severity.NORMAL)
    async def test_homepage_logo_and_heading(self, home):
        allure.step("Open homepage and verify key UI is visible")
        await expect(home.logo).to_be_visible()
        await expect(home.hero_text).to_be_visible()

        allure.step("Basic sanity: page title present")
        title = await home.title()
        assert isinstance(title, str) and len(title) > 0
