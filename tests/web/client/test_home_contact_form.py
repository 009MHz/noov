import pytest
import allure
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
@allure.feature("Home/ Contact Form")
@pytest.mark.ui
@pytest.mark.smoke
class TestContactForm:
    @allure.title("Contact Form Validation Invalid handler")
    @allure.severity(severity.NORMAL)
    @pytest.mark.parametrize(
        "scenario, name, email, message",
        [
            ("empty", "", "", ""),
            ("invalid_name", "", "qa@test.com", "Test Message"),
            ("invalid_email", "QA Test", "invalid_email", "Test Message"),
            ("invalid_message", "QA Test", "qa@test.com", ""),
        ],
    )
    async def test_contact_form_error_validation(
        self, home, scenario, name, email, message, platform
    ):
        with step(f"Submit form with {scenario} scenario"):
            if scenario == "empty":
                await home.click_send_message()
                with step("Verify all error messages are visible"):
                    await expect(home.err_name).to_be_visible()
                    await expect(home.err_email).to_be_visible()
                    await expect(home.err_message).to_be_visible()
            else:
                await home.fill_contact_form(name=name, email=email, message=message)
                await home.click_send_message()

                with step(f"Verify error message for {scenario}"):
                    if scenario == "invalid_name":
                        await expect(home.err_name).to_be_visible()
                    elif scenario == "invalid_email":
                        await expect(home.err_email).to_be_visible()
                    elif scenario == "invalid_message":
                        await expect(home.err_message).to_be_visible()

    @allure.title("Contact Form - Successful Submission")
    @allure.severity(severity.CRITICAL)
    async def test_contact_form_submit_happy_path(self, home, platform):
        with step("Fill form with valid data"):
            await home.fill_contact_form(
                name="QA Test",
                email="test@QA.com",
                message="Hello team, this is a test message from Playwright.",
            )

        with step("Submit the completed form"):
            await home.click_send_message()

        with step("Verify the error message is not displayed"):
            await expect(home.err_name).not_to_be_visible()
            await expect(home.err_email).not_to_be_visible()
            await expect(home.err_message).not_to_be_visible()
