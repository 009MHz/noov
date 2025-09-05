import pytest
import allure
import re
from playwright.async_api import expect
from sources.web.client.home_page import HomePage
from allure import severity_level as severity
from utils.allure_helpers import step


@pytest.fixture(scope="function")
async def home(page):
    home = HomePage(page)
    await home.open()
    return home


@allure.epic("Marketing Site")
@allure.feature("Homepage")
@pytest.mark.ui
class TestHomeSmoke:
    @allure.title("Homepage Smoke Test - Logo and Heading")
    @allure.feature("Home/ Heading")
    @allure.severity(severity.NORMAL)
    async def test_language_toggle(self, page, home, platform):
        with step("Click on the language toggle and verify URL change to Indonesian"):
            await expect(home.language_toggle).to_contain_text("Indonesian")
            await home.click_language_toggle()
            await expect(page).to_have_url(re.compile(r".*/id"))
            await expect(home.language_toggle).to_contain_text("English")

        with step("Click again the language toggle and verify URL change to English"):
            await home.click_language_toggle()
            await expect(page).not_to_have_url(re.compile(r".*/id"))
            await expect(home.language_toggle).to_contain_text("Indonesian")

        with step("Click the main Logo icon"):
            await home.click_main_logo()
            await expect(page).to_have_url(re.compile(r".*#home"))

    @allure.title("Homepage Mobile Banner validation")
    @allure.feature("Home/ Mobile Banner")
    @allure.severity(severity.CRITICAL)
    @pytest.mark.parametrize("market", ["Apple", "Google"])
    async def test_mobile_app_redirection(self, page, home, market, platform):
        if market == "Apple":
            with step(f"Click on the {market} button"):
                await home.click_banner_apple_btn()
            with step(f"Verify the {market} redirection"):
                await expect(page).to_have_url(
                    re.compile(
                        r"https://apps.apple.com/id/app/ucollect-by-noovoleum/.*"
                    )
                )
        else:
            with step(f"Click on the {market} button"):
                await home.click_banner_android_btn()
            with step(f"Verify the {market} redirection"):
                await expect(page).to_have_url(
                    "https://play.google.com/store/apps/details?id=com.noovoleum.ucollect"
                )
