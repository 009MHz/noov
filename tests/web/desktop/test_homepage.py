import re

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

    async def test_homepage_language_toggle(self, home):
        allure.step("Open homepage and verify language toggle is visible")
        await expect(home.language_toggle).to_be_visible()
        await expect(home.language_toggle).to_contain_text("Indonesian")
        await expect(home.language_toggle).to_be_enabled()

    async def test_homepage_mobile_banner(self, home):
        allure.step("Open homepage and verify mobile app banner is visible")
        await expect(home.banner_mobile).to_be_visible()
        await expect(home.apple_btn).to_have_attribute("href", re.compile(r"noovoleum\.onelink\.me"))
        await expect(home.android_btn).to_have_attribute("href", re.compile(r"noovoleum\.onelink\.me"))

    async def test_homepage_form_submit(self, home):
        allure.step("Open homepage contact section and verify form validation")
        await expect(home.header_submit).to_be_visible()
        await expect(home.input_name).to_be_visible()
        await expect(home.input_email).to_be_visible()
        await expect(home.input_message).to_be_visible()
        await expect(home.btn_send).to_be_visible()

    async def test_homepage_company_information(self, home):
        allure.step("Open homepage and verify company information")
        await expect(home.info_logo).to_be_visible()
        await expect(home.company_sg_address).to_be_visible()
        await expect(home.company_id_address).to_be_visible()
        await expect(home.linkedin_link).to_have_attribute("href", re.compile(r"linkedin\.com/company/noovoleum"))
        await expect(home.instagram_link).to_have_attribute("href", re.compile(r"instagram\.com/noovoleumid"))
        await expect(home.email_link).to_be_visible()
