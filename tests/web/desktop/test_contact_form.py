import pytest
import allure
from playwright.async_api import expect
from sources.web.home_page import HomePage

CONTACT_URL = "https://noovoleum.com#contact"

@allure.epic("Marketing Site")
@allure.feature("Contact Form")
@pytest.mark.asyncio
async def test_contact_form_shows_validation_when_empty_submit(page):
    home = HomePage(page)

    with allure.step("Open Contact section"):
        await home.open_contact(CONTACT_URL)

    with allure.step("Submit without filling any fields"):
        await home.submit_contact()

    with allure.step("Expect validation errors on all required fields"):
        await home.expect_validation_errors()


@allure.epic("Marketing Site")
@allure.feature("Contact Form")
@pytest.mark.asyncio
async def test_contact_form_submit_happy_path(page):
    home = HomePage(page)

    with allure.step("Open Contact section"):
        await home.open_contact(CONTACT_URL)

    with allure.step("Fill valid inputs"):
        await home.fill_contact_form(
            name="Haris Satriyo",
            email="qa@example.com",
            message="Hello team, this is a test message from Playwright async.",
        )

    with allure.step("Submit the form"):
        await home.submit_contact()

    with allure.step("Verify success indicator (adjust selector/text to your app)"):
        # Replace with your actual success state (toast/snackbar/alert)
        success = page.get_by_text("Message sent").first
        await expect(success).to_be_visible()
