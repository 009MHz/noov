import pytest, allure
import re
from playwright.async_api import expect
from sources.web.home_page import HomePage
from allure import severity_level as severity


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
    async def test_language_toggle(self, page, home):
        allure.step("Click on the language toggle and verify URL change to Indonesian")
        await expect(home.language_toggle).to_contain_text("Indonesian")
        await home.click_language_toggle()
        await expect(page).to_have_url(re.compile(r".*/id"))
        await expect(home.language_toggle).to_contain_text("English")

        allure.step("Click again the language toggle and verify URL change to English")
        await home.click_language_toggle()
        await expect(page).not_to_have_url(re.compile(r".*/id"))
        await expect(home.language_toggle).to_contain_text("Indonesian")

        allure.step("Click the main Logo icon")
        await home.click_main_logo()
        await expect(page).to_have_url(re.compile(r".*#home"))

    @allure.title("Homepage Mobile Banner validation")
    @allure.feature("Home/ Mobile Banner")
    @allure.severity(severity.CRITICAL)
    @pytest.mark.parametrize("platform", ["iOS", "Android"])
    async def test_mobile_app_redirection(self, page, home, platform):
        allure.step(f"Click on the {platform} button")
        if platform == "iOS":
            await home.click_banner_apple_btn()
            await expect(page).to_have_url(re.compile(r"https://apps.apple.com/id/app/ucollect-by-noovoleum/.*"))
        else:
            await home.click_banner_android_btn()
            await expect(page).to_have_url("https://play.google.com/store/apps/details?id=com.noovoleum.ucollect")