import pytest
import allure
from allure import severity_level
from sources.mobile.android.chrome_screen import ChromeScreen
from utils.allure_helpers import step


@allure.epic("Mobile Testing")
@allure.feature("Chrome Browser Search")
@pytest.mark.mobile
@pytest.mark.android
class TestMobileChromeSearch:
    """Simple test class for Chrome browser search functionality."""

    @allure.title("Chrome Browser: Search for 'Appium' and verify results")
    @allure.severity(severity_level.CRITICAL)
    async def test_chrome_search_appium(self, android_driver):
        chrome = ChromeScreen(android_driver)

        with step("1. Search for 'Appium' using omnibox flow"):
            await chrome.search_keyword("Appium")

        with step("2. Verify the URL redirection contains keyword"):
            assert chrome.url_redirection("Appium")

        with step("3. Verify search results are not empty"):
            assert chrome.verify_results_not_empty()
