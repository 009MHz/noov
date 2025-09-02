import pytest
import allure
from playwright.async_api import expect
from sources.web.home_page import HomePage
from allure import severity_level as severity

CONTACT_URL = "https://noovoleum.com#contact"

@pytest.fixture(scope='function')
async def contact_page(page):
    home = HomePage(page)
    await home.open_contact(CONTACT_URL)
    return home

@allure.epic("Marketing Site")
@allure.feature("Contact Form")
@pytest.mark.ui
@pytest.mark.smoke
class TestContactForm:
    @allure.title("Contact Form Validation - Empty Submit")
    @allure.severity(severity.NORMAL)
    @pytest.mark.asyncio
    async def test_contact_form_shows_validation_when_empty_submit(self, contact_page):
        allure.step("Submit form without filling any fields")
        await contact_page.submit_contact()

        allure.step("Verify validation errors on all required fields")
        await contact_page.expect_validation_errors()

    @allure.title("Contact Form - Successful Submission")
    @allure.severity(severity.CRITICAL)
    @pytest.mark.asyncio
    async def test_contact_form_submit_happy_path(self, contact_page):
        allure.step("Fill form with valid data")
        await contact_page.fill_contact_form(
            name="Haris Satriyo",
            email="qa@example.com",
            message="Hello team, this is a test message from Playwright async.",
        )

        allure.step("Submit the completed form")
        await contact_page.submit_contact()

        allure.step("Verify success message appears")
        success = contact_page.page.get_by_text("Message sent").first
        await expect(success).to_be_visible()
