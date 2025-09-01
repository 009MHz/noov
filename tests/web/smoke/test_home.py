import pytest
from libs.config_loader import load_settings
from sources.web.home_page import HomePage
from playwright.async_api import expect

@pytest.mark.ui
@pytest.mark.smoke
async def test_home_hero_and_logo(page):
    s = load_settings()
    hp = HomePage(page)
    await hp.goto(s.base_url)
    await expect(hp.hero_heading).to_be_visible()
    await expect(hp.logo).to_be_visible()

@pytest.mark.ui
async def test_language_toggle_switches_path(page):
    s = load_settings()
    hp = HomePage(page)
    await hp.goto(s.base_url)
    await hp.toggle_language()
    # Clicking 'Indonesian' should go to '/id'
    await expect(page).to_have_url(lambda url: url.endswith("/id"))

@pytest.mark.ui
async def test_contact_form_required_errors(page):
    s = load_settings()
    hp = HomePage(page)
    await hp.goto(s.base_url + "#contact")
    await hp.send_message_btn.click()
    await expect(hp.name_error).to_have_text("Name is required")
    await expect(hp.email_error).to_have_text("Email is required")
    await expect(hp.message_error).to_have_text("Message is required")

@pytest.mark.ui
async def test_contact_form_invalid_email(page):
    s = load_settings()
    hp = HomePage(page)
    await hp.goto(s.base_url + "#contact")
    await hp.name_input.fill("QA Bot")
    await hp.email_input.fill("not-an-email")
    await hp.message_textarea.fill("Hello from automation")
    await hp.send_message_btn.click()
    await expect(hp.email_error).to_have_text("Email must be valid")
