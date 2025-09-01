import pytest
import allure
from playwright.sync_api import Page
from sources.web.home_page import HomePage

@pytest.mark.ui
@pytest.mark.smoke
@allure.title("Homepage shows logo and hero heading")
def test_homepage_logo_and_heading(page: Page):
    HomePage(page).open().assert_hero_and_logo()

@pytest.mark.ui
@allure.title("Language toggle switches to Indonesian path")
def test_language_toggle(page: Page):
    HomePage(page).open().toggle_language().assert_switched_to_indonesian()

@pytest.mark.ui
@allure.title("Contact form shows required errors when empty")
def test_contact_form_required_errors(page: Page):
    HomePage(page).open_contact().submit_contact().assert_required_errors()

@pytest.mark.ui
@allure.title("Contact form validates email format")
def test_contact_form_invalid_email(page: Page):
    HomePage(page).open_contact().submit_contact(
        name="QA Bot", email="not-an-email", message="Hello from automation"
    ).assert_invalid_email_error()
