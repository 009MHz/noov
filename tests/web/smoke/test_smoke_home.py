import pytest, allure
from playwright.async_api import Page
from sources.web.home_page import HomePage

@pytest.mark.ui
@pytest.mark.smoke
@allure.title("Homepage shows logo and hero heading")
async def test_homepage_logo_and_heading(page: Page):
    await HomePage(page).open()
    await HomePage(page).assert_hero_and_logo()

@pytest.mark.ui
@allure.title("Language toggle switches to Indonesian path")
async def test_language_toggle(page: Page):
    home = HomePage(page)
    await home.open()
    await home.toggle_language()
    await home.assert_switched_to_indonesian()

@pytest.mark.ui
@allure.title("Contact form shows required errors when empty")
async def test_contact_form_required_errors(page: Page):
    home = HomePage(page)
    await home.open_contact()
    await home.submit_contact()
    await home.assert_required_errors()

@pytest.mark.ui
@allure.title("Contact form validates email format")
async def test_contact_form_invalid_email(page: Page):
    home = HomePage(page)
    await home.open_contact()
    await home.submit_contact(name="QA Bot", email="not-an-email", message="Hello")
    await home.assert_invalid_email_error()